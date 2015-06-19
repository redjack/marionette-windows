import os

import marionette_windows.util


class BaseTask(object):
    def do_task(self):
        assert False

    def is_successful(self):
        assert False

    def get_desc(self):
        assert False


class MakeBinDirTask(BaseTask):
    # This creates the bin dir that we use for staging compiled packages.

    def __init__(self):
        self.directory_to_create_ = os.path.join(os.getenv('INSTDIR'),'bin')

    def get_desc(self):
        return "Creating directory " + self.directory_to_create_

    def do_task(self):
        marionette_windows.util.create_directory(self.directory_to_create_)

    def is_successful(self):
        return os.path.exists(self.directory_to_create_)


class MakeLibDirTask(BaseTask):
    # This creates the lib dir that we use for staging compiled packages.

    def __init__(self):
        self.directory_to_create_ = os.path.join(os.getenv('INSTDIR'),'lib')

    def get_desc(self):
        return "Creating directory " + self.directory_to_create_

    def do_task(self):
        marionette_windows.util.create_directory(self.directory_to_create_)

    def is_successful(self):
        return os.path.exists(self.directory_to_create_)


class InstallPrereqsTask(BaseTask):
    # - Add the wine ppa, because we need wine >=1.5, not available
    #   in the standard repos.
    # - Do an update first
    # - Install all our required dependencies
    def __init__(self):
        self.packages_to_install = ['libgmp-dev',
                               'python-pip',
                               'python-dev',
                               'git',
                               'm4',
                               'zip',
                               'unzip',
                               'subversion',
                               'faketime',
                               'g++-mingw-w64',
                               'gcc-mingw-w64',
                               'mingw-w64',
                               'wine1.6',
                               'p7zip-full']

    def do_task(self):
        marionette_windows.util.execute(
            "sudo add-apt-repository -y ppa:ubuntu-wine/ppa")

        marionette_windows.util.execute(
            "sudo apt-get -y update")

        for package in self.packages_to_install:
            marionette_windows.util.execute(
                "sudo apt-get --no-install-recommends " + \
                              "-y install "+package)

    def get_desc(self):
        return 'Installing required packages'

    def is_successful(self):
        retcodes = []
        for package in self.packages_to_install:
            retcodes.append(marionette_windows.util.execute('sudo dpkg -S '+package))
        return len(retcodes) > 0 and \
               max(retcodes) == 0 and \
               min(retcodes) == 0


class InitWineTask(BaseTask):
    # Initialize our Wine environment

    def do_task(self):
        marionette_windows.util.execute(
            'LD_PRELOAD= wineboot -i')

    def get_desc(self):
        return 'Initializing Wine'

    def is_successful(self):
        return os.path.exists(
            '/home/vagrant/.wine')


class InstallPythonTask(BaseTask):
    def do_task(self):
        file_path = marionette_windows.util.download_file(
            'https://www.python.org/ftp/python/2.7.5/python-2.7.5.msi')
        marionette_windows.util.msi_install(
            file_path, os.path.join(
                os.path.join(os.getenv('INSTDIR'),'python')))

    def get_desc(self):
        return 'Installing Python'

    def is_successful(self):
        return os.path.exists(
            os.path.join(os.getenv('INSTDIR'),'python', 'python.exe')
        )


class InstallSetuptoolsTask(BaseTask):
    def do_task(self):
        file_path = marionette_windows.util.download_file(
            'https://pypi.python.org/packages/source/s/setuptools/setuptools-17.1.1.tar.gz')
        marionette_windows.util.python_package_install(
            file_path)

    def get_desc(self):
        return 'Installing setuptools'

    def is_successful(self):
        os.chdir(os.getenv('VAGRANTDIR'))
        retcode = marionette_windows.util.execute(
            "LD_PRELOAD= $INSTPYTHON -c 'import setuptools'")
        return (retcode == 0)


class InstallPy2EXETask(BaseTask):
    def do_task(self):
        os.chdir(os.getenv('BUILDDIR'))
        marionette_windows.util.execute(
            'cp ../thirdparty/py2exe-0.6.9.win32-py2.7.exe .')

        os.chdir(os.path.dirname(file_path))
        file_name = os.path.basename(file_path)
        marionette_windows.util.execute(
            '7z x %s' % file_name)
        retval = marionette_windows.util.execute(
            'cp -a PLATLIB/* $INSTDIR/python/Lib/site-packages/')

        return retval

    def get_desc(self):
        return 'Installing py2exe'

    def is_successful(self):
        os.chdir(os.getenv('VAGRANTDIR'))
        retcode = marionette_windows.util.execute(
            "LD_PRELOAD= $INSTPYTHON -c 'import py2exe'")
        return (retcode == 0)


class InstallWineWrappers(BaseTask):
    def do_task(self):
        os.chdir(os.getenv('BUILDDIR'))
        marionette_windows.util.execute(
            'cp -rvf ../thirdparty/wine-wrappers .')
        os.chdir(os.path.join(os.getenv('BUILDDIR'),'wine-wrappers'))
        marionette_windows.util.execute(
            'mkdir -p build/bdist.win32/winexe/bundle-2.7/')
        marionette_windows.util.execute(
            'cp -a $INSTDIR/python/python27.dll build/bdist.win32/winexe/bundle-2.7/')
        marionette_windows.util.execute(
            'LD_PRELOAD= $INSTPYTHON setup.py py2exe')
        marionette_windows.util.execute(
            'cp -a dist/gcc.exe dist/g++.exe dist/dllwrap.exe dist/swig.exe $WINEROOT/windows/')

    def get_desc(self):
        return 'Installing wine-wrappers'

    def is_successful(self):
        return os.path.exists(
            os.path.join(os.getenv('WINEROOT'),'windows','g++.exe'))


class InstallDlfcnTask(BaseTask):
    def do_task(self):
        dir_path = marionette_windows.util.git_clone(
            'https://github.com/dlfcn-win32/dlfcn-win32.git')
        os.chdir(dir_path)
        marionette_windows.util.execute(
            './configure --cc=i686-w64-mingw32-gcc --cross-prefix=i686-w64-mingw32- --prefix=$INSTDIR/mingw')
        marionette_windows.util.execute('make')
        marionette_windows.util.execute('make install')

    def get_desc(self):
        return 'Installing dlfcn'

    def is_successful(self):
        return os.path.exists(
            os.path.join(os.getenv('INSTDIR'),'mingw','include','dlfcn.h'))


class InstallMmanTask(BaseTask):
    def do_task(self):
        dir_path = marionette_windows.util.svn_checkout(
            'http://mman-win32.googlecode.com/svn/trunk', 'mman-win32')
        os.chdir(dir_path)
        marionette_windows.util.execute('chmod 755 configure')
        marionette_windows.util.execute(
            './configure --cc=i686-w64-mingw32-gcc --cross-prefix=i686-w64-mingw32-'
            ' --prefix=$INSTDIR/mingw'
            ' --libdir=$INSTDIR/mingw/lib'
            ' --incdir=$INSTDIR/mingw/include'
        )
        marionette_windows.util.execute('make')
        marionette_windows.util.execute('make install')

    def get_desc(self):
        return 'Installing mman'

    def is_successful(self):
        return os.path.exists(
            os.path.join(os.getenv('INSTDIR'),'mingw','include','mman.h'))

class Generic(BaseTask):
    def do_task(self):
        pass

    def get_desc(self):
        return 'Installing setuptools'

    def is_successful(self):
        pass