# GMP
GMPFILE=gmp-6.0.0a.tar.bz2
cd $BUILDDIR
if [ ! -e $GMPFILE ]
then
  wget http://ftp.gnu.org/gnu/gmp/$GMPFILE
fi
tar xvf $GMPFILE
cd gmp-*
LD_PRELOAD=/usr/lib/faketime/libfaketime.so.1 ./configure --prefix=$INSTDIR/gmp --host=i686-w64-mingw32 --enable-cxx --disable-static --enable-shared
#find -type f -print0 | xargs -0 touch --date="$FAKETIME"
make
make install
