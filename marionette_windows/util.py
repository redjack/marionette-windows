import os
import os.path
import string
import urllib2

debug = False


def create_directory(dir_path):
    if debug:
        print ' - creating dir %s' % dir_path

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return True


def execute(cmd):
    if debug:
        print ' - executing cmd: "%s"' % cmd

    retval = os.system("%s >> %s 2> %s" % (cmd,
                                         '$VAGRANTDIR/marionette_windows.log',
                                         '$VAGRANTDIR/marionette_windows.err.log'))

    return int(retval)


def download_file(url):
    basename = os.path.basename(url)
    retval = os.path.join(os.getenv('BUILDDIR'), basename)
    if not os.path.exists(retval):
        if debug:
            print ' - downloading: "%s"' % url

        response = urllib2.urlopen(url)
        with open(retval, 'w') as fh:
            fh.write(response.read())

    return retval


def git_clone(url):
    basename = os.path.basename(url)
    basename = remove_extension(basename)
    retval = os.path.join(os.getenv('BUILDDIR'), basename)
    if not os.path.exists(retval):
        if debug:
            print ' - git cloning: "%s"' % url

        execute('git clone %s %s' % (url, retval))

    return retval


def svn_checkout(url, dest_dir=None):
    if not dest_dir:
        basename = os.path.basename(url)
        basename = remove_extension(basename)
        retval = os.path.join(os.getenv('BUILDDIR'), basename)
    else:
        retval = os.path.join(os.getenv('BUILDDIR'), dest_dir)

    if not os.path.exists(retval):
        if debug:
            print ' - svn checkout: "%s"' % url

        execute('svn checkout %s %s' % (url, retval))

    return retval


def msi_install(msi_path, dst_dir):
    if debug:
        print ' - msi install: "%s"' % msi_path

    retval = execute(
        'LD_PRELOAD= msiexec /qn /i %s TARGETDIR=%s' % (msi_path, dst_dir))
    return retval


def python_package_install(file_path):
    if debug:
        print ' - python package install: "%s"' % file_path

    dst_dir = remove_extension(file_path)
    os.chdir(os.path.dirname(file_path))
    if file_path.endswith('.zip'):
        execute('unzip %s' % (file_path))
    else:
        execute('tar xvf %s %s' % (file_path, dst_dir))
    os.chdir(dst_dir)
    execute(
        'LD_PRELOAD= $INSTPYTHON setup.py build_ext -c mingw32')
    retval = execute(
        'LD_PRELOAD= $INSTPYTHON setup.py install')

    return retval

def remove_extension(file_path):
    retval = os.path.basename(file_path)
    retval = string.replace(retval, '.tar.gz','')
    retval = string.replace(retval, '.zip','')
    retval = string.replace(retval, '.git','')
    return retval