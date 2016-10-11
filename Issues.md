# Known Issues and Resolutions

## Installation failure: No Python.h error message

Issue overview is  
* OS: Ubuntu 14.04.4 LTS (Bash on windows)
* Issue Type: Installation failure

Get the following error message, then azuresshconfig installtion fail
```
 c/_cffi_backend.c:2:20: fatal error: Python.h: No such file or directory
```

A resolution is to install python header package before azuresshconfig install
```
sudo apt-get install python2.7-dev
sudo pip install azhresshconfig
```




