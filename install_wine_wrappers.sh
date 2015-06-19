cd $BUILDDIR
cp -rvf $VAGRANTDIR/thirdparty/wine-wrappers .
cd $BUILDDIR/wine-wrappers
find -type f -print0 | xargs -0 touch --date="$FAKETIME"
# Push our config into wine-wrappers.
> settings.py
echo "LD_PRELOAD = \"$LD_PRELOAD\"" >> settings.py
echo "FAKETIME = \"$FAKETIME\"" >> settings.py
# Must pre-copy python27.dll into the build directory, or else py2exe can't find it.
mkdir -p build/bdist.win32/winexe/bundle-2.7/
cp -a $INSTDIR/python/python27.dll build/bdist.win32/winexe/bundle-2.7/
LD_PRELOAD= $INSTPYTHON setup.py py2exe
cp -a dist/gcc.exe dist/g++.exe dist/dllwrap.exe dist/swig.exe $WINEROOT/windows/
cd ..
