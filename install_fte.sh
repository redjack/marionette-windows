# FTE
cd $BUILDDIR
if [ ! -e libfte ]
then
  git clone https://github.com/kpdyer/libfte.git
fi
cd libfte
#find -type f -print0 | xargs -0 touch --date="$FAKETIME"
ln -s $INSTDIR/gmp thirdparty/gmp
cp -a $INSTDIR/gmp/bin/libgmp-10.dll .
LD_PRELOAD= WINDOWS_BUILD=1 CROSS_COMPILE=1 PYTHON=$INSTPYTHON make
LD_PRELOAD= $INSTPYTHON setup.py install
