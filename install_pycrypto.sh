cd $BUILDDIR
if [ ! -e pycrypto-2.6.1.tar.gz ]
then
  wget https://ftp.dlitz.net/pub/dlitz/crypto/pycrypto/pycrypto-2.6.1.tar.gz
fi
gzip -d pycrypto-2.6.1.tar.gz
tar xvf pycrypto-2.6.1.tar
cd pycrypto-*
ac_cv_func_malloc_0_nonnull=yes sh configure --host=i686-w64-mingw32
LD_PRELOAD= $INSTPYTHON setup.py build_ext -c mingw32
LD_PRELOAD= $INSTPYTHON setup.py install
