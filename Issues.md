# Known Issues and Resolutions

## Installation failure: No Python.h error message

Issue overview is  
* OS: Ubuntu 14.04.4 LTS
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


## Execution failure: SNIMissingWarning and InsecurePlatformWarning error message

Issue overview is  
* OS: Ubuntu 14.04.4 LTS
* Issue Type: Execution failure

Get the following error message while azuresshconfig executing
```
/usr/local/lib/python2.7/dist-packages/requests/packages/urllib3/util/ssl_.py:318: SNIMissingWarning: An HTTPS request has been made, but the SNI (Subject Name Indication) extension to TLS is not available on this platform. This may cause the server to present an incorrect TLS certificate, which can cause validation failures. You can upgrade to a newer version of Python to solve this. For more information, see https://urllib3.readthedocs.io/en/latest/security.html#snimissingwarning.
  SNIMissingWarning

/usr/local/lib/python2.7/dist-packages/requests/packages/urllib3/util/ssl_.py:122: InsecurePlatformWarning: A true SSLContext object is not available. This prevents urllib3 from configuring SSL appropriately and may cause certain SSL connections to fail. You can upgrade to a newer version of Python to solve this. For more information, see https://urllib3.readthedocs.io/en/latest/security.html#insecureplatformwarning.
  InsecurePlatformWarning
```

A resolution is to install pyOpenSSL ndg-httpsclient pyasn1 package
```
pip install pyOpenSSL ndg-httpsclient pyasn1
```
See also Stackoverflow:[SSL InsecurePlatform error when using Requests package](http://stackoverflow.com/questions/29099404/ssl-insecureplatform-error-when-using-requests-package)


