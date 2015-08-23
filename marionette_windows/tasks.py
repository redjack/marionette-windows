import os

import marionette_windows.util


def clone_regex2dfa():
    version = '351fc169facb3f8b43d2d10bbef826119328ff11'
    dir_path = marionette_windows.util.git_clone(
        'https://github.com/kpdyer/regex2dfa.git')
    os.chdir(dir_path)

    # Use the non-CFFI version of regex2dfa.git
    marionette_windows.util.execute(
        'git checkout %s' % version)
    return dir_path


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
    # Do an install of Python 2.7.5 from the MSI.

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
    # Install setuptools from source, required for py2exe

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
    # Install py2exe, required to build wine-wrappers
    # We can't build py2exe from source, b/c that would require
    # the wine-wrappers. Maybe there's a better way?

    def do_task(self):
        os.chdir(os.getenv('BUILDDIR'))
        marionette_windows.util.execute(
            'cp ../thirdparty/py2exe-0.6.9.win32-py2.7.exe .')
        marionette_windows.util.execute(
            '7z x py2exe-0.6.9.win32-py2.7.exe')
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
    # The wine wrappers are needed to expose gcc/g++/etc
    # to our Python build env. This creates gcc.exe, and
    # under the hood calls our mingw compiler.

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
    # Required for openfst

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
    # Required for re2

    def do_task(self):
        dir_path = marionette_windows.util.svn_checkout(
            'http://mman-win32.googlecode.com/svn/trunk', 'mman-win32')
        os.chdir(dir_path)
        marionette_windows.util.execute('chmod 755 configure')
        marionette_windows.util.execute(
            './configure --cc=i686-w64-mingw32-gcc --cross-prefix=i686-w64-mingw32-'
            ' --prefix=$INSTDIR/mingw'
            ' --libdir=$INSTDIR/mingw/lib'
            ' --incdir=$INSTDIR/mingw/include/sys'
        )
        marionette_windows.util.execute('make')
        marionette_windows.util.execute('make install')

    def get_desc(self):
        return 'Installing mman'

    def is_successful(self):
        return os.path.exists(
            os.path.join(os.getenv('INSTDIR'),'mingw','include','sys','mman.h'))


class InstallRegex2DFATask_openfst(BaseTask):
    # Building openfst from regex2dfa

    def do_task(self):
        clone_regex2dfa()

        marionette_windows.util.execute(
            'patch -R third_party/openfst/src/lib/mapped-file.cc ../../patches/openfst.patch')

        os.chdir('third_party/openfst')
        marionette_windows.util.execute(
            './configure CFLAGS=\'-fPIC\' CXXFLAGS=\'-fPIC\' --enable-bin --enable-static --disable-shared --host=i686-w64-mingw32')
        marionette_windows.util.execute(
            'sed -i \'s/-lm -ldl/-lm -ldl -lmman -lpsapi/g\' src/bin/Makefile')
        marionette_windows.util.execute(
            'make')

    def get_desc(self):
        return 'Installing regex2dfa.openfst'

    def is_successful(self):
        return os.path.exists(
            os.path.join(os.getenv('BUILDDIR'),'regex2dfa',
                         'third_party/openfst/src/lib/.libs/libfst.a'))

class InstallRegex2DFATask_re2(BaseTask):
    # This is messy, but we use a win32 version of re2
    # and patch it to use our compilers. It doesn't provide
    # a way to override and ignores CC, CXX env. variables, etc.

    def do_task(self):
        os.chdir(os.getenv('BUILDDIR'))
        marionette_windows.util.execute(
            'cp ../thirdparty/re2-20110930-src-win32.zip .')
        if not os.path.exists('re2'):
            marionette_windows.util.execute(
                'unzip re2-20110930-src-win32.zip')
            marionette_windows.util.execute(
                'cp $BUILDDIR/../patches/re2-*.patch .')
            marionette_windows.util.execute(
                'patch --verbose -p0 -i re2-core.patch')
            marionette_windows.util.execute(
                'patch --verbose -p0 -i re2-mingw.patch')
        os.chdir('re2')
        marionette_windows.util.execute(
            'make obj/libre2.a')
        os.makedirs(
            os.path.join(
                os.getenv('BUILDDIR'),
                'regex2dfa/third_party/re2/obj'))
        marionette_windows.util.execute(
            'cp $BUILDDIR/re2/obj/libre2.a'
              ' $BUILDDIR/regex2dfa/third_party/re2/obj')

    def get_desc(self):
        return 'Installing regex2dfa.re2'

    def is_successful(self):
        return os.path.exists(
            os.path.join(os.getenv('BUILDDIR'),'regex2dfa',
                         'third_party/re2/obj/libre2.a'))

class InstallRegex2DFATask(BaseTask):
    # This is messy, we probably want to turn it into a single patch
    # Comments inline

    def do_task(self):
        clone_regex2dfa()

        marionette_windows.util.execute(
            './configure --prefix=$INSTDIR/regex2dfa')
        if not os.path.exists('regex2dfa.patched'):
            # pthread is optional, disabling reduces features in regex2dfa
            marionette_windows.util.execute(
                'sed -i \'s/-pthread//g\' Makefile')

            # make sure we have our POSIX libs included directly
            marionette_windows.util.execute(
                'sed -i \'s/-ldl/-ldl -lmman -lpsapi/g\' Makefile')

            # regex2dfa hardcodes ar
            marionette_windows.util.execute(
                'sed -i \'s/ ar / $(AR) /g\' Makefile')

            # stdint is required under mingw for unint32_t
            marionette_windows.util.execute(
                'sed -i \'s/#include <Python.h>/#include <Python.h>\\n#include <stdint.h>/g\' src/cRegex2dfa.cc')

            # these hardening flags don't work under mingw
            marionette_windows.util.execute(
                'sed -i "s/\'-fstack-protector-all\',//g" setup.py')
            marionette_windows.util.execute(
                'sed -i "s/\'-D_FORTIFY_SOURCE\',//g" setup.py')
            marionette_windows.util.execute(
                'sed -i "s/\'-fPIE\',//g" setup.py')

            # regex2dfa setup.py libs are all messed up and hardcoded
            marionette_windows.util.execute(
                'sed -i "s/\'python2.7\',/\'mman\',\'dl\',\'psapi\'/g" setup.py')
            marionette_windows.util.execute(
                'sed -i "s/library_dirs=\[\'\.libs\'\],/library_dirs=[\'.libs\',\'\/home\/vagrant\/install\/mingw\/lib\'],/g" setup.py')

            # signal that we've patched regex2dfa
            marionette_windows.util.execute(
                'touch regex2dfa.patched')

            # ensure that libre2.a has a timestamp that's ahead
            # of $(RE2_DIR)/util/logging.h.fixed
            # this is a bug in regex2dfa, which manifests itself in how we do our build
            # and reflects that logging.h.fixed is a dependency of libre2.a in regex2dfa's Makefile
            marionette_windows.util.execute(
                'touch $BUILDDIR/regex2dfa/third_party/re2/util/logging.h.fixed')
            marionette_windows.util.execute(
                'touch $BUILDDIR/regex2dfa/third_party/re2/obj/libre2.a')

        marionette_windows.util.execute(
            'make')
        marionette_windows.util.execute(
            'LD_PRELOAD= $INSTPYTHON setup.py build_ext -c mingw32')
        marionette_windows.util.execute(
            'LD_PRELOAD= $INSTPYTHON setup.py install')

    def get_desc(self):
        return 'Installing regex2dfa'

    def is_successful(self):
        os.chdir(os.getenv('VAGRANTDIR'))
        retcode = marionette_windows.util.execute(
            "LD_PRELOAD= $INSTPYTHON -c 'import regex2dfa'")
        return (retcode == 0)

class InstallGMPTask(BaseTask):
    # easy: build/install GMP under mingw

    def do_task(self):
        file_path = marionette_windows.util.download_file(
            'http://ftp.gnu.org/gnu/gmp/gmp-6.0.0a.tar.bz2')
        marionette_windows.util.configure_install(
            file_path,
            'LD_PRELOAD=/usr/lib/faketime/libfaketime.so.1 ./configure --prefix=$INSTDIR/gmp --host=i686-w64-mingw32 --enable-cxx --disable-static --enable-shared')
        marionette_windows.util.execute(
            'cp -a $INSTDIR/gmp/bin/libgmp-10.dll $WINEROOT/windows/system32/')

    def get_desc(self):
        return 'Installing GMP'

    def is_successful(self):
        return os.path.exists(
            os.path.join(os.getenv('INSTDIR'),
                         'gmp/bin/libgmp-10.dll'))


class InstallPyCryptoTask(BaseTask):
    # easy: build/install pycrypto under mingw

    def do_task(self):
        file_path = marionette_windows.util.download_file(
            'https://ftp.dlitz.net/pub/dlitz/crypto/pycrypto/pycrypto-2.6.1.tar.gz')
        marionette_windows.util.python_package_install(
            file_path,
            'ac_cv_func_malloc_0_nonnull=yes sh configure --host=i686-w64-mingw32')

    def get_desc(self):
        return 'Installing pycrypto'

    def is_successful(self):
        os.chdir(os.getenv('VAGRANTDIR'))
        retcode = marionette_windows.util.execute(
            "LD_PRELOAD= $INSTPYTHON -c 'import Crypto'")
        return (retcode == 0)

class InstallPyCurl(BaseTask):
    # Install py2exe, required to build wine-wrappers
    # We can't build py2exe from source, b/c that would require
    # the wine-wrappers. Maybe there's a better way?

    def do_task(self):
        os.chdir(os.getenv('BUILDDIR'))
        marionette_windows.util.execute(
            'cp ../thirdparty/pycurl-7.19.5.1.win32-py2.7.exe .')
        marionette_windows.util.execute(
            '7z x pycurl-7.19.5.1.win32-py2.7.exe')
        retval = marionette_windows.util.execute(
            'cp -a PLATLIB/* $INSTDIR/python/Lib/site-packages/')

        return retval

    def get_desc(self):
        return 'Installing pycurl'

    def is_successful(self):
        os.chdir(os.getenv('VAGRANTDIR'))
        retcode = marionette_windows.util.execute(
            "LD_PRELOAD= $INSTPYTHON -c 'import pycurl'")
        return (retcode == 0)

class InstallFTETask(BaseTask):
    # easy: build/install FTE under mingw

    def do_task(self):
        dir_path = marionette_windows.util.git_clone(
            'https://github.com/kpdyer/libfte.git')
        os.chdir(dir_path)
        marionette_windows.util.execute(
            'ln -s $INSTDIR/gmp thirdparty/gmp'
        )
        marionette_windows.util.execute(
            'LD_PRELOAD= WINDOWS_BUILD=1 CROSS_COMPILE=1 PYTHON=$INSTPYTHON make')
        marionette_windows.util.execute(
            'LD_PRELOAD= $INSTPYTHON setup.py install')

    def get_desc(self):
        return 'Installing FTE'

    def is_successful(self):
        os.chdir(os.getenv('VAGRANTDIR'))
        retcode = marionette_windows.util.execute(
            "LD_PRELOAD= $INSTPYTHON -c 'import fte'")
        return (retcode == 0)



class InstallMarionetteTask(BaseTask):
    # finally: build/install marionette under mingw

    def do_task(self):
        dir_path = marionette_windows.util.git_clone(
            'https://github.com/redjack/marionette.git')
        os.chdir(dir_path)
        marionette_windows.util.execute(
            'LD_PRELOAD= $INSTPYTHON setup.py install')

    def get_desc(self):
        return 'Installing marionette'

    def is_successful(self):
        os.chdir(os.getenv('VAGRANTDIR'))
        retcode = marionette_windows.util.execute(
            "LD_PRELOAD= $INSTPYTHON -c 'import marionette_tg'")
        return (retcode == 0)
