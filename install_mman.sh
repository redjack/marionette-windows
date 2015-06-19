MMANDIR=mman-win32
cd $BUILDDIR
if [ ! -e $MMANDIR ]
then
  svn checkout http://mman-win32.googlecode.com/svn/trunk/ mman-win32
fi
cd mman-win32
#find -type f -print0 | xargs -0 touch --date="$FAKETIME"
chmod 755 configure
./configure --cc=i686-w64-mingw32-gcc --cross-prefix=i686-w64-mingw32- --prefix=$INSTDIR/mingw --libdir=$INSTDIR/mingw/lib --incdir=$INSTDIR/mingw/include/sys
make
make install
