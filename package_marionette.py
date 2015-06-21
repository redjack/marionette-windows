import os
import sys

import marionette_windows.util

marionette_windows.util.debug = False

# The goal here is to create a single zipfile with
# all exes, dlls, etc. required to run marionette_client.exe
# and marionette_server.exe on modern windows.

def build_exes():
    os.chdir(
        os.path.join(os.getenv('BUILDDIR'), 'marionette')
    )
    os.makedirs('build/bdist.win32/winexe/bundle-2.7')
    marionette_windows.util.execute(
        'cp -a /home/vagrant/install/python/python27.dll build/bdist.win32/winexe/bundle-2.7/'
    )
    marionette_windows.util.execute(
        'LD_PRELOAD= $INSTPYTHON setup.py py2exe'
    )
    assert os.path.exists(
        os.path.join(os.getenv('BUILDDIR'), 'marionette',
                     'dist', 'marionette_server.exe')
    )

def make_package():
    os.chdir(
        os.path.join(os.getenv('BUILDDIR'), 'marionette', 'dist')
    )
    marionette_windows.util.execute(
        'cp /home/vagrant/install/gmp/bin/libgmp-10.dll .'
    )
    marionette_windows.util.execute(
        'cp /home/vagrant/install/python/python27.dll .'
    )
    os.makedirs(
        'marionette_tg/formats'
    )
    marionette_windows.util.execute(
        'cp -rfv ../marionette_tg/formats/* marionette_tg/formats/'
    )
    marionette_windows.util.execute(
        'cp ../marionette_tg/marionette.conf marionette_tg/'
    )
    marionette_windows.util.execute(
        'cp /home/vagrant/install/python/Lib/site-packages/marionette_tg-0.0.1.post6-py2.7.egg/marionette_tg/parsetab.* marionette_tg'
    )
    marionette_windows.util.execute(
        'zip -q -9 -r marionette.zip marionette_tg/parsetab.pyc'
    )
    marionette_windows.util.execute(
        'rm marionette_tg/parsetab.*'
    )
    marionette_windows.util.execute(
        'zip -r marionette-latest.zip *'
    )
    marionette_windows.util.execute(
        'mkdir -p $VAGRANTDIR/dist'
    )
    marionette_windows.util.execute(
        'cp marionette-latest.zip $VAGRANTDIR/dist/'
    )

    assert os.path.exists(
        os.path.join(os.getenv('VAGRANTDIR'), 'dist',
                     'marionette-latest.zip')
    )

def main():
    if not os.getenv('BUILDDIR'):
        print 'Are you sure your envs are set? Run \'source setenv.sh\' in /vagrant.'
        sys.exit(1)

    os.chdir(os.getenv('VAGRANTDIR'))
    retcode = marionette_windows.util.execute(
        "LD_PRELOAD= $INSTPYTHON -c 'import marionette_tg'")
    if (retcode != 0):
        print 'Looks like marionette hasn\'t been built yet.'
        sys.exit(1)

    build_exes()
    make_package()

    marionette_zip = os.path.join(os.getenv('VAGRANTDIR'), 'dist',
                     'marionette-latest.zip')
    if os.path.exists(marionette_zip):
        print '**** SUCCESS: zipfile located at:', marionette_zip
    else:
        print '!!!! Somethinge went wrong, we failed to make the zipfile...check marionette_windows.log'

if __name__ == '__main__':
    main()
