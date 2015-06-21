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
marionette-latest.zip
```

Upon success, the ```vagrant up``` command should produce a zipfile in ```dist/marionette-latest.zip``` which has all the dependencies (.pyc, .pyd, .dll files) required to run marionette, and two binaries ```marionette_client.exe``` and ```marionette_server.exe```.

In the build machines ```bootstrap.sh``` is executed which invokes ```build_marionette.py``` and ```package_marionette.py```. These two scripts install marionette in the VM and create the zip.

dependencies
------------

* Vagrant
* An Ubuntu box. This has been tested with version 20150611.0.0 of ```ubuntu/precise32```, provided by hashicorp.
  * To install use ```vagrant box add ubuntu/precise32```

important scripts
-----------------

* *build_marionette.py* runs all tasks in marionette_windows.tasks that are required to run marionette.
* *package_marrionete.py* once we have all deps. installed, this will create a zip with all the dependencies and our exes.
* *marionette_windows/tasks.py* has all of the tasks we run. ```do_task``` has the logic for each task (create dir, compile somthing, etc.) and ```is_successful``` checks if ```do_task``` completeled properly.
