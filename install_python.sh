cd $BUILDDIR
PYTHONMSI=python-2.7.5.msi
if [ ! -e $PYTHONMSI ]
then
  wget https://www.python.org/ftp/python/2.7.5/$PYTHONMSI
fi
LD_PRELOAD= msiexec /qn /i $PYTHONMSI TARGETDIR=$INSTDIR/python
sed -i 's/self.dll_libraries = get_msvcr()/pass#self.dll_libraries = get_msvcr()/g' $INSTDIR/python/Lib/distutils/cygwinccompiler.py
cd $INSTDIR/python
find -type f -print0 | xargs -0 touch --date="$FAKETIME"
