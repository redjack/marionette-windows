R2DDIR=regex2dfa
cd $BUILDDIR
if [ ! -e $R2DDIR ]
then
  git clone https://github.com/kpdyer/regex2dfa.git
fi

cd $VAGRANTDIR
patch -R build/regex2dfa/third_party/openfst/src/lib/mapped-file.cc openfst.patch

cd $BUILDDIR/regex2dfa/third_party/openfst/
./configure CFLAGS='-fPIC' CXXFLAGS='-fPIC' --enable-bin --enable-static --disable-shared --host=i686-w64-mingw32
sed -i 's/-lm -ldl/-lm -ldl -lmman -lpsapi/g' src/bin/Makefile
make

cd $BUILDDIR
cp $BUILDDIR/../thirdparty/re2-20110930-src-win32.zip .
unzip re2-20110930-src-win32.zip
cp $BUILDDIR/../re2-*.patch .
patch --verbose -p0 -i re2-core.patch
patch --verbose -p0 -i re2-mingw.patch
cd re2
make obj/libre2.a
mkdir -p $BUILDDIR/regex2dfa/third_party/re2/obj
cp $BUILDDIR/re2/obj/libre2.a $BUILDDIR/regex2dfa/third_party/re2/obj

cd $BUILDDIR/regex2dfa
./configure --prefix=$INSTDIR/regex2dfa
sed -i 's/-pthread//g' Makefile
sed -i 's/-ldl/-ldl -lmman -lpsapi/g' Makefile
sed -i 's/ ar / $(AR) /g' Makefile
sed -i 's/#include <Python.h>/#include <Python.h>\n#include <stdint.h>/g' src/cRegex2dfa.cc
sed -i "s/'-fstack-protector-all',//g" setup.py
sed -i "s/'-D_FORTIFY_SOURCE',//g" setup.py
sed -i "s/'-fPIE',//g" setup.py
sed -i "s/'python2.7',/'mman','dl','psapi'/g" setup.py
sed -i "s/library_dirs=\['\.libs'\],/library_dirs=['.libs','\/home\/vagrant\/install\/mingw\/lib'],/g" setup.py
#find -type f -print0 | xargs -0 touch --date="$FAKETIME"
touch $BUILDDIR/regex2dfa/third_party/re2/obj/libre2.a
make 
LD_PRELOAD= $INSTPYTHON setup.py build_ext -c mingw32
LD_PRELOAD= $INSTPYTHON setup.py install
