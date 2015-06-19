DLFCNDIR=dlfcn-win32
cd $BUILDDIR
if [ ! -e $DLFCNDIR ]
then
  git clone https://github.com/dlfcn-win32/dlfcn-win32.git
fi
cd dlfcn-win32
#find -type f -print0 | xargs -0 touch --date="$FAKETIME"
./configure --cc=i686-w64-mingw32-gcc --cross-prefix=i686-w64-mingw32- --prefix=$INSTDIR/mingw
make
make install
