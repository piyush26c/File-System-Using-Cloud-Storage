# Implementation of a standard file system that uses Google Cloud storage object.

Usually, file systems are implemented inside the OS kernel. However, it is possible to implement them in userspace. FUSE is a File system in User Space.

If a directory is mounted using FUSE, the kernel "forwards" the FS system calls to the user-space FUSE handler. The main challenge is to implement and handle the various FS calls.

Implementation provided in this repository solves the challenge using the component [libfuse](https://github.com/libfuse/libfuse).

### Understanding the FUSE:
![alt text](https://github.com/piyush26c/File-System-Using-Cloud-Storage/blob/main/diagrams/fuseexplain.png)


<br>

### Architecture Diagram:
![alt text](https://github.com/piyush26c/File-System-Using-Cloud-Storage/blob/main/diagrams/design.png)

`GCSFuse.py` is the main file that contains the implementation.
<br>
`install_requirements.sh` file will install all required dependencies in your local machine / VM (depending on user).


<br>

**How to setup the environment to run the code?**

  1. I personally developed this code using VM because, as a user, I need sudo access to mount and unmount the local directories which luddy servers wont' provide.
  2. If you want to test the code on/using VM, then just execute the bash script provided with submission named as `start_setup.sh` file. This bash script will create a VM, SSH into VM and last download and install all required dependencies. That's it, you are ready to execute the code. After you execute all the required material and review you can run the `stop_setup.sh` to stop and delete the vm.
  3. If you want to test the code on your local Linux machine, do not execute the `start_setup.sh` bash script; instead, copy the code provided (/eccfsassignment.zip) into your machine, unzip the code, and execute the following commands(this will install the dependencies.).
        - `cd eccfsassignment`
        - `chmod +x install_requirements.sh`
        - `sudo ./install_requirements.sh`

<br>
    
**After setting up the environment how to execute the code and which file?**

  1. `GCSFuse.py` is the main file that contains the file system code.
  2. Open first terminal and execute the main file by using the following command.
  
     `$python3 GCSFuse.py <local_folder_name> <google_cloud_bucket_storage_name> <mount_folder_name>`
     
     In screenshots, pasted in report, I have executed following command, where `google_cloud_bucket_storage_name=eccfsbucket` is already created on my account. Also, the `local_folder_name=local_folder` and `mount_folder_name=mount_folder` are created inside the `/eccfsassignment` folder.
     
     `$python3 GCSFuse.py local_folder eccfsbucket mount_folder`
     
  2. First terminal will be stuck after executing the above command, meaning, the file system code is running!
  
  3. Further, open another new terminal, and perform `cd eccfsassignment/<mount_folder_name>`, in this `mount_folder_name` directory you can see all the files and directories present in GCS bucket and here you can execute different File System Calls.
  
  4. To know which call is performed after a particular file system call, I have logged those calls in a file named `logsinfo.log`. You can see the sequence of the function calls performed by the `GCSFuse.py` file.
  
  5. Here in this second terminal, you can run any linux command, however there are few calls (eg. close(), sync(), flush(), readdir(), opendir()) for whom we can see whether the system call was invoked or not. To check if does actually my implementation correctly invokes the required call, I have written a `test.py` file. You can run this `test.py` file by being in `eccfsassignment/` directory by executing this command `:~/eccfsassignment$python3 test.py`. This command will print output on console/terminal and you can check the correctness accordingly.
  
