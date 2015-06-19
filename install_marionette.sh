# FTE
cd $BUILDDIR
if [ ! -e marionette ]
then
  git clone https://github.com/rejack/marionette.git
fi
cd marionette
cp $INSTDIR/gmp/bin/libgmp-10.dll .
LD_PRELOAD= $INSTPYTHON setup.py install
LD_PRELOAD= $INSTPYTHON marionette_tg/dsl_tests.py
LD_PRELOAD= $INSTPYTHON marionette_tg/record_layer_tests.py
