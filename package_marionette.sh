cd $BUILDDIR/marionette
rm -rfv build dist marionette_tg.egg-info
mkdir -p build/bdist.win32/winexe/bundle-2.7
cp -a /home/vagrant/install/python/python27.dll build/bdist.win32/winexe/bundle-2.7/
LD_PRELOAD= $INSTPYTHON setup.py py2exe

cd $BUILDDIR/marionette/dist
cp /home/vagrant/install/gmp/bin/libgmp-10.dll .
cp /home/vagrant/install/python/python27.dll .
cp -rfv ../marionette_tg marionette_tg
mkdir tmp
mv marionette.zip tmp
cd tmp
unzip marionette.zip
cp -rfv ../marionette_tg/* marionette_tg/
cp /home/vagrant/install/python/Lib/site-packages/marionette_tg-0.0.1.post6-py2.7.egg/marionette_tg/parsetab.* marionette_tg
rm marionette.zip
zip -r marionette.zip *
mv marionette.zip ..
cd ..
rm marionette_tg/*.py tmp marionette_tg/plugins
zip -r marionette-latest.zip *
rm -f *.exe *.dll marionette.zip marionette_tg
mkdir -p $VAGRANTDIR/dist
cp marionette-latest.zip $VAGRANTDIR/dist/