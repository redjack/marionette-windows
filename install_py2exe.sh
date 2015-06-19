cd $BUILDDIR
cp $VAGRANTDIR/thirdparty/py2exe-* .
7z x py2exe-0.6.9.win32-py2.7.exe
cp -a PLATLIB/* $INSTDIR/python/Lib/site-packages/
