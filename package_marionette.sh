cd $BUILDDIR/marionette
rm -rfv build dist marionette_tg.egg-info
mkdir -p build/bdist.win32/winexe/bundle-2.7
cp -a /home/vagrant/install/python/python27.dll build/bdist.win32/winexe/bundle-2.7/
LD_PRELOAD= $INSTPYTHON setup.py py2exe

#mkdir -p $BUILDDIR/marionette/dist/marionette-latest
cd $BUILDDIR/marionette/dist
#mv *.zip marionette-latest/
#mv *.exe marionette-latest/
#cd $BUILDDIR/marionette/dist/marionette-latest
cp /home/vagrant/install/gmp/bin/libgmp-10.dll .
cp /home/vagrant/install/python/python27.dll .
cp -rfv ../marionette_tg marionette_tg
mkdir tmp
mv marionette.zip tmp
cd tmp
unzip marionette.zip
cp -rfv ../marionette_tg/* marionette_tg/
cp /home/vagrant/install/python/Lib/site-packages/marionette_tg-0.0.1.post6-py2.7.egg/marionette_tg/parsetab.py marionette_tg
cp /home/vagrant/install/python/Lib/site-packages/marionette_tg-0.0.1.post6-py2.7.egg/marionette_tg/parsetab.pyc marionette_tg
rm marionette.zip
zip -r marionette.zip *
mv marionette.zip ..
cd ..
rm -rfv marionette_tg/plugins
rm marionette_tg/*.py
rm -rfv tmp
zip -r marionette-latest.zip *
rm -rvf marionette_tg
rm -f marionette.zip
rm -f *.exe
rm -f *.dll
#LD_PRELOAD= wine marionette_server.exe 127.0.0.1 1234 dummy
