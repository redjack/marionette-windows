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
    if not os.path.exists('build/bdist.win32/winexe/bundle-2.7'):
        os.makedirs('build/bdist.win32/winexe/bundle-2.7')
    marionette_windows.util.execute(
        'cp -a /home/vagrant/install/python/python27.dll build/bdist.win32/winexe/bundle-2.7/'
    )
    for script in ('bin/marionette_server', 'bin/marionette_client'):
        marionette_windows.util.execute(
            'LD_PRELOAD= $INSTPYTHON -m PyInstaller.main --onefile --clean ' +
            '--hidden-import=zope.interface --hidden-import=_cffi_backend ' +
            script
        )
    assert os.path.exists(
        os.path.join(os.getenv('BUILDDIR'), 'marionette',
                     'dist', 'marionette_server.exe')
    )
    assert os.path.exists(
        os.path.join(os.getenv('BUILDDIR'), 'marionette',
                     'dist', 'marionette_client.exe')
    )

def make_package():
    os.chdir(
        os.path.join(os.getenv('BUILDDIR'), 'marionette', 'dist')
    )

    # we must have the python interpreter
    marionette_windows.util.execute(
        'cp /home/vagrant/install/python/python27.dll .'
    )

    # we need to include libgmp-10.dll next to the exes
    #   for FTE
    marionette_windows.util.execute(
        'cp /home/vagrant/install/gmp/bin/libgmp-10.dll .'
    )

    # include all our formats
    if not os.path.exists('marionette_tg/formats'):
        os.makedirs(
            'marionette_tg/formats'
        )
    marionette_windows.util.execute(
        'cp -rfv ../marionette_tg/formats/* marionette_tg/formats/'
    )

    # include our marionette.conf file
    marionette_windows.util.execute(
        'cp ../marionette_tg/marionette.conf marionette_tg/'
    )

    # add dsl.py to marionette.zip, b/c it's required
    #   for PLY to compile at runtime
    marionette_windows.util.execute(
        'cp ../marionette_tg/dsl.py marionette_tg/'
    )
    marionette_windows.util.execute(
        'zip -q -9 -r marionette.zip marionette_tg/dsl.py'
    )
    marionette_windows.util.execute(
        'rm marionette_tg/dsl.py'
    )

    # add {libcurl.dll,msvcr90.dll} to marionette.zip
    marionette_windows.util.execute(
        'cp $INSTDIR/python/Lib/site-packages/libcurl.dll .'
    )
    marionette_windows.util.execute(
        'cp $INSTDIR/python/msvcr90.dll .'
    )
    marionette_windows.util.execute(
        'zip -q -9 -r marionette.zip libcurl.dll'
    )
    marionette_windows.util.execute(
        'zip -q -9 -r marionette.zip msvcr90.dll'
    )
    marionette_windows.util.execute(
        'rm -f libcurl.dll msvcr90.dll'
    )

    # add regex2dfa/{psapi.dll,msvcr90.dll} to marionette.zip
    marionette_windows.util.execute(
        'mkdir regex2dfa'
    )
    marionette_windows.util.execute(
        'cp $WINEROOT/windows/system32/psapi.dll regex2dfa/'
    )
    marionette_windows.util.execute(
        'cp $INSTDIR/python/msvcr90.dll regex2dfa/'
    )
    marionette_windows.util.execute(
        'zip -q -9 -r marionette.zip regex2dfa'
    )
    marionette_windows.util.execute(
        'rm -rf regex2dfa'
    )

    # bundle all files into marionette-latest.zip
    marionette_windows.util.execute(
        'zip -r marionette-latest.zip *'
    )

    # move marionette-latest.zip to our dist dir
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
