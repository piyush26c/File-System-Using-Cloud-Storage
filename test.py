import os
import shutil
print("test code executing...")

mount_folder_name = "mount_folder"
file_name = "testfile.txt"
path = mount_folder_name + '/' + file_name

if os.path.exists(path):
    os.remove(path)
    print(f"Deleted existing {path}")

# Creating a file name testfile.txt and writing a content to it
with open(path, 'w') as file:
    file.write('Hello Students, I am Piyush Chaudhari.')

print(f"Content has been written to {path}")

# Read the content from file
with open(path, 'r') as file:
    read_content = file.read()
    print("Content read from the file:")
    print(read_content)

# with statement implicitly invokes the release file sytem call where I close the file.

# creating a folder
directory_path = f"{mount_folder_name}/folder1"
os.mkdir(directory_path)
print("Directory created (True/False):", os.path.exists(directory_path))

# deleting a folder and its contents
print("Deletign the directory ...", directory_path)
shutil.rmtree(directory_path)
print("Directory not deleted successfully (True/False):", os.path.exists(directory_path))

# delete a file
file_to_delete = f"{mount_folder_name}/file_to_delete.txt"
with open(file_to_delete, 'w') as file:
    file.write('Hello Students, I am Piyush Chaudhari.\nFile to delete it is.')

if os.path.exists(file_to_delete):
    os.remove(file_to_delete)
    print(f"{file_to_delete} has been successfully deleted.")
else:
    print(f"{file_to_delete} does not exist.")

# renaming

# rename a file
old_file_name = f"{mount_folder_name}/old_file.txt"
new_file_name = f"{mount_folder_name}/new_file.txt"

# creating two files
with open(old_file_name, 'w') as file:
    file.write('Hello Students, I am Piyush Chaudhari.')

with open(new_file_name, 'w') as file:
    file.write('Hello Students, I am Piyush Chaudhari.')

# Check if the file exists before renaming
if os.path.exists(old_file_name):
    os.rename(old_file_name, new_file_name)
    print(f"Renamed {old_file_name} to {new_file_name}")
else:
    print(f"{old_file_name} does not exist.")


# rename a folder
old_folder_name = f"{mount_folder_name}/old_folder"
new_folder_name = f"{mount_folder_name}/new_folder"

if os.path.exists(old_folder_name):
    shutil.rmtree(old_folder_name)
if os.path.exists(new_folder_name):
    shutil.rmtree(new_folder_name)

os.mkdir(old_folder_name)
os.mkdir(new_folder_name)

# check if the folder exists before renaming
if os.path.exists(old_folder_name):
    os.rename(old_folder_name, new_folder_name)
    print(f"Renamed {old_folder_name} to {new_folder_name}")
else:
    print(f"{old_folder_name} does not exist.")


print("test code execution complete.")

# sudo fio --filename=normal_exec.txt --size=1GB --rw=rw --direct=1 --bs=32k --ioengine=libaio --runtime=60 --numjobs=1 --time_based --group_reporting --name=normal_seqrw --iodepth=16