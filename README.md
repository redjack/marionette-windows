# marionette-windows

This is a project that's used to build build marionette for windows. We use a combination of mingw and wine within a VM to do the build process.

quickstart
----------

```console
git clone git@github.com:kpdyer/marionette-windows-builder.git
cd marionette-windows-builder/build
git clone git@github.com:redjack/marionette.git
cd ..
vagrant up
... wait ...
ls -al dist
marionette-latest.zip
```

dependencies
------------

* Vagrant
* An Ubuntu box. This has been tested with ```ubuntu/precise32```.
  * To install use ```vagrant box add ubuntu/precise32```
