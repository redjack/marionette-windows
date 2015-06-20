# marionette-windows

This is a project that's used to build build marionette for windows. We use a combination of mingw and wine within a VM to do the build process.

quickstart
----------

Given that marionette is a private repo we need to clone it manually.

*** note: this build can take 20-30 minutes ***

```console
$ git clone git@github.com:kpdyer/marionette-windows-builder.git
$ cd marionette-windows-builder/build
$ git clone git@github.com:redjack/marionette.git
$ cd ..
$ vagrant up

... wait ...

$ ls -al dist
$ marionette-latest.zip
```

dependencies
------------

* Vagrant
* An Ubuntu box. This has been tested with version 20150611.0.0 of ```ubuntu/precise32```, provided by hashicorp.
  * To install use ```vagrant box add ubuntu/precise32```
