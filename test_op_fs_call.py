# testing only open() file system call
mounted_folder_name = "mount_folder"
file = open(f'{mounted_folder_name}/file1.txt', 'w')
# print(file.read())
file.write("Hello bunty!")