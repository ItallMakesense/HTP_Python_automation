# Tests description #
* * *
## test_owner.py ##

This testcase includes two test functions, that check, if different users on an NFS client can access shared nfs folder, configured to read and write access only for **_one user_**

#### Steps ####
1. Configures local and remote hosts to be NFS client and server accordingly:
    - Installs virtual environment (with necessary packages), from which runs
      test command, that:
        - Creates test user on local host
        - Creates testing folders on both sides
        - Installs nfs utils on local and remote hosts, configuring server's exports file

2. Creates test file on NFS server and mounts test folder to the NFS client

3. In `test_existing_user` method, tries to edit test file by user, from which module was runned. If operation was successfull, test is **_passed_**. If not, test is **_failed_**

4. In `test_new_user` method, tries to edit test file by test user, that was created during nfs client creation. If operation was successfull, test is **_failed_**. If not, test is **_passed_**

5. Unmounts test folder from NFS client and removes test file, if it still exists

6. Restores starting conditions:
    - Removes test user from local host
    - Removes test folders on local and remote hosts
    - Removes any lines, added to exports file, on remote host
    - Removes nfs utils on local and remote hosts
    - Removes virtual environment on local host
* * *
## test_ro_access.py ##

This testcase includes three test methods, that check, if user on an NFS client can create, edit and delete files in shared nfs folder, configured to **_read only_** access

#### Steps ####
1. Configures local and remote hosts to be NFS client and server accordingly:
    - Installs virtual environment (with necessary packages), from which runs
      test command, that:
        - Creates testing folders on both sides
        - Installs nfs utils on local and remote hosts, configuring server's exports file

2. Creates test file on NFS server and mounts test folder to the NFS client

3. In `test_creation` method, tries to create new file. If operation was successfull, test is **_failed_**. If not, test is **_passed_**

3. In `test_edition` method, tries to edit test file. If operation was successfull, test is **_failed_**. If not, test is **_passed_**

4. In `test_deletion` method, tries to remove test file. If operation was successfull, test is **_failed_**. If not, test is **_passed_**

5. Unmounts test folder from NFS client and removes test file, if it still exists

6. Restores starting conditions:
    - Removes test folders on local and remote hosts
    - Removes any lines, added to exports file, on remote host
    - Removes nfs utils on local and remote hosts
    - Removes virtual environment on local host
* * *
## test_rw_access.py ##

This testcase includes three test methods, that check, if user on an NFS client can create, edit and delete files in shared nfs folder, configured to **_read and write_** access

#### Steps ####
1. Configures local and remote hosts to be NFS client and server accordingly:
    - Installs virtual environment (with necessary packages), from which runs
      test command, that:
        - Creates testing folders on both sides
        - Installs nfs utils on local and remote hosts, configuring server's exports file

2. Creates test file on NFS server and mounts test folder to the NFS client

3. In `test_creation` method, tries to create new file. If operation was successfull, test is **_passed_**. If not, test is **_failed_**

3. In `test_edition` method, tries to edit test file. If operation was successfull, test is **_passed_**. If not, test is **_failed_**

4. In `test_deletion` method, tries to remove test file. If operation was successfull, test is **_passed_**. If not, test is **_failed_**

5. Unmounts test folder from NFS client and removes test file, if it still exists

6. Restores starting conditions:
    - Removes test folders on local and remote hosts
    - Removes any lines, added to exports file, on remote host
    - Removes nfs utils on local and remote hosts
    - Removes virtual environment on local host
