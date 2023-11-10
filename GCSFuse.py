#!/usr/bin/env python

from __future__ import with_statement

import os
import sys
import errno
import time

from fuse import FUSE, FuseOSError, Operations, LoggingMixIn
from google.cloud import storage
import logging


class GCSFuse(LoggingMixIn, Operations):
    def __init__(self, root, gcs_bucket_name):
        self.root = root
        self.client = storage.Client.from_service_account_json('piyush-chaudhari-fall2023-8f85ee7dc13d.json')
        self.gcs_bucket_name = gcs_bucket_name
        self.bucket = self.client.get_bucket(self.gcs_bucket_name)
        
        # checking if bucket already exists?
        if not self.bucket:
            self.bucket = self.client.create_bucket(self.bucket_name, location='US-EAST1')
        
        self.sync_mount_local_bucket()

    def sync_mount_local_bucket(self):
        '''
        Downloads the files and directories from Google Cloud Storage to specified mount_folder location.
        '''

        blobs = list(self.bucket.list_blobs())
        for blob in blobs:
            local_path = os.path.join(self.root, blob.name)
            if local_path.endswith('/'):
                os.makedirs(local_path, exist_ok=True)
            else:
                # Download the object if it's a file
                os.makedirs(os.path.dirname(local_path), exist_ok=True)
                blob.download_to_filename(local_path)

    # Helpers
    # =======

    def _full_path(self, partial):
        # print("_full_path:", partial)
        partial = partial.lstrip("/")
        path = os.path.join(self.root, partial)
        return path

    # Filesystem methods
    # ==================

    def access(self, path, mode):
        # print("access(), ", path, mode)
        full_path = self._full_path(path)
        if not os.access(full_path, mode):
            raise FuseOSError(errno.EACCES)

    # def chmod(self, path, mode):
    #     full_path = self._full_path(path)
    #     return os.chmod(full_path, mode)

    # def chown(self, path, uid, gid):
    #     full_path = self._full_path(path)
    #     return os.chown(full_path, uid, gid)

    def getattr(self, path, fh=None):
        logging.info("getattr() called.")
        # print("getattr(), ", path)
        full_path = self._full_path(path)
        st = os.lstat(full_path)
        return dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime',
                     'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid'))

    def readdir(self, path, fh):
        # print("readdir(), ", path, fh)
        full_path = self._full_path(path)

        dirents = ['.', '..']
        if os.path.isdir(full_path):
            dirents.extend(os.listdir(full_path))
        for r in dirents:
            yield r

    def readlink(self, path):
        # print("readlink(), ", path)
        pathname = os.readlink(self._full_path(path))
        if pathname.startswith("/"):
            # Path name is absolute, sanitize it.
            return os.path.relpath(pathname, self.root)
        else:
            return pathname

    def mknod(self, path, mode, dev):
        # print("mknod(), ", path, mode, dev)
        return os.mknod(self._full_path(path), mode, dev)

    def rmdir(self, path):
        # print("rmdir(), ", path)
        full_path = self._full_path(path)
        # print("rmdir() is called full path", full_path)
        # for gcs bucket
        prefix = path[1:]
        for blob in self.bucket.list_blobs(prefix=prefix):
            blob.delete()

        return os.rmdir(full_path)

    def mkdir(self, path, mode):
        # print("mkdir(), ", path, mode)
        blob = self.bucket.blob(path[1:] + "/")
        blob.upload_from_string("")
        return os.mkdir(self._full_path(path), mode)

    def opendir(self, path):
        'Returns a numerical file handle.'
        # print("opendir(), ", path)
        return os.open(self._full_path(path), os.O_DIRECTORY | os.O_RDONLY)
    
    def statfs(self, path):
        # print("statfs(), ", path)
        full_path = self._full_path(path)
        stv = os.statvfs(full_path)
        return dict((key, getattr(stv, key)) for key in ('f_bavail', 'f_bfree',
            'f_blocks', 'f_bsize', 'f_favail', 'f_ffree', 'f_files', 'f_flag',
            'f_frsize', 'f_namemax'))

    def unlink(self, path):
        '''
        unlink is used to remove(delete) a file from the file system.
        '''
        # print("unlink(), ", path)
        # removing from gcs bucket
        # reference: https://cloud.google.com/storage/docs/deleting-objects#storage-delete-object-python
        generation_match_precondition = None
        blob = self.bucket.blob(path[1:])
        if blob.exists():
            blob.reload()  # fetch blob metadata to use in generation_match_precondition.
            generation_match_precondition = blob.generation
            blob.delete(if_generation_match=generation_match_precondition)
        
        # print("unlink called", path, "status: ", status)
        return os.unlink(self._full_path(path))

    def symlink(self, name, target):
        # print("symlink(), ", name, target)
        return os.symlink(name, self._full_path(target))

    def rename(self, old, new):
        # print("rename(), ", old, new)
        status = os.rename(self._full_path(old), self._full_path(new))

        old_prefix = old[1:]
        new_prefix = new[1:]
        objects_to_rename = list(self.bucket.list_blobs(prefix=old_prefix))
        # print(objects_to_rename)

        if (len(objects_to_rename) > 0):
            # its a directory
            old_itself_indx = -1
            for indx in range(len(objects_to_rename)):
                blob = objects_to_rename[indx]
                new_blob_name = new_prefix + blob.name[len(old_prefix):]
                if blob.name[len(old_prefix):] == '/':
                    old_itself_indx = indx
                    continue
                # Copy the content from the old object to the new object
                new_blob = self.bucket.blob(new_blob_name)
                new_blob.upload_from_string(blob.download_as_string())        
                # Delete the old object
                blob.delete()

            if (old_itself_indx != -1):
                objects_to_rename[old_itself_indx].delete()

        else:
            # logic only for file
            source_blob = self.bucket.blob(old[1:])
            blob_copy = self.bucket.copy_blob(source_blob, self.client.bucket(self.gcs_bucket_name), new[1:])
            self.bucket.delete_blob(old[1:])

        return status

    def link(self, target, name):
        # print("link(), ", target, name)
        return os.link(self._full_path(target), self._full_path(name))

    def utimens(self, path, times=None):
        # print("utimens(), ", path)
        return os.utime(self._full_path(path), times)

    # File methods
    # ============

    def open(self, path, flags):
        # print("open(), ", path)
        full_path = self._full_path(path)
        return os.open(full_path, flags)

    def create(self, path, mode, fi=None):
        # print("create(), ", path)
        # logging.debug("path:")
        blob = self.bucket.blob(path[1:])
        # time.sleep(1)
        blob.upload_from_string("")
        full_path = self._full_path(path)
        return os.open(full_path, os.O_WRONLY | os.O_CREAT, mode)

    def read(self, path, length, offset, fh):
        # print("read(), ", path, length, offset, fh)
        os.lseek(fh, offset, os.SEEK_SET)
        return os.read(fh, length)

    def write(self, path, buf, offset, fh):
        # print("write(), ", path, buf, offset, fh)
        os.lseek(fh, offset, os.SEEK_SET)
        written = os.write(fh, buf)
        blob = self.bucket.blob(path[1:])
        full_path = self._full_path(path)

        # To ensure data consistency, upload the entire file content from the local cache
        with open(full_path, 'rb') as local_file:
            # time.sleep(1)
            blob.upload_from_file(local_file)

        return written

    def truncate(self, path, length, fh=None):
        # print("truncate(), ", path, length)
        full_path = self._full_path(path)
        with open(full_path, 'r+') as f:
            f.truncate(length)

    def flush(self, path, fh):
        '''
        Clears buffers for this stream and causes any buffered data to be written to the file.
        '''
        # print("flush(), ", path, fh)
        return os.fsync(fh)

    def release(self, path, fh):
        # print("release(), ", path, fh)
        return os.close(fh)

    def fsync(self, path, fdatasync, fh):
        # print("fsync(), ", path, fdatasync, fh)
        return self.flush(path, fh)


def mount(gcs_bucket_name, local_folder, mount_folder):
    print("mounting ....")
    FUSE(GCSFuse(local_folder, gcs_bucket_name), mount_folder, nothreads=True, foreground=True)

if __name__ == '__main__':
    logging.basicConfig(filename="logsinfo.log", level=logging.INFO)
    # logging.basicConfig(filename="logsdebug.log", level=logging.DEBUG)
    local_folder = sys.argv[1]
    gcs_bucket_name = sys.argv[2]
    mount_folder = sys.argv[3]
    mount(gcs_bucket_name, local_folder, mount_folder)