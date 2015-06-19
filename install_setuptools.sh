cd $BUILDDIR
if [ ! -e setuptools-17.1.1.tar.gz ]
then
  wget https://pypi.python.org/packages/source/s/setuptools/setuptools-17.1.1.tar.gz
fi
tar xvf setuptools-17.1.1.tar.gz
cd setuptools-*
find -type f -print0 | xargs -0 touch --date="$FAKETIME"
LD_PRELOAD= $INSTPYTHON setup.py install
