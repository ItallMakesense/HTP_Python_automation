# NFS_test #

## Package for testing basic functional of the NFS file sharing system ##
* * *
### Overwiew ###

This package by default tests three test cases:
- User access permission for shared folder
- Read only permission for shared folder
- Read and write permission for shared folder

NFS_test uses `pytest` module to do the testing.

During tests local computer would be nfs client,
while remote computer - nfs server.

Works with python version 2.7+.

Though it's essential to also have pip package manager,
assosiated with already installed python, on a local host.

All the information, captured during testing,
will be available at `logs` folder (by default).

> _Note_: This test will take around 400 seconds... Yeah, pretty bad, but the explanation exists - NFS 90-second grace period:
  >> "The purpose of the grace period is to give the clients enough time to notice that the server has rebooted, and to reclaim their existing locks without danger of having somebody else steal the lock from them."

> NFS installation is prodused every time new test case begins, so: 90 * 3 = 270.

> That is the 270 seconds of just... waiting.

### How to use ###

First you need to configurate package execution, using `config.py`.

It's necessary at least to provide local host address, remote host address
(that would correspond that host's name, see /ets/hosts) and available user name,
and passwords for both local and remote hosts (to provide superuser privilegues).
Other information is optional.

Some of it can be configured directly in command line, using these options
(default names are given):
- `--client_pass` - for local host password
- `--server_pass` - for remote host password
- `--client_dir` - for testing directory (mount folder) on a local host
- `--server_dir` - for testing directory (mounted folder) on a remote host
- `--test_file` - for specifying name of file, that would be created
- `--test_user` - for specifying name of user, that would be created

To run all the tests, simply enter:
```
$: python pytest_nfs.py
```
It will find all the tests under `tests` folder and do them.

To run one test:
```
$: python pytest_nfs.py tests/test_owner.py
```

To run two tests... well, better simply ignore one of them:
```
$: python pytest_nfs.py --ignore=test_owner.py
```

To specify password options:
```
$: python pytest_nfs.py --client_pass=no --server_pass=way
```

To execute only one test in test case:
```
$: python pytest_nfs.py tests/test_ro_access.py -k=test_creation
```
