#!/bin/bash

cd /vagrant
source ./setenv.sh
cd $VAGRANTDIR && source ./mkdirs.sh
cd $VAGRANTDIR && source ./install_prereqs.sh
cd $VAGRANTDIR && source ./init_wine.sh
cd $VAGRANTDIR && source ./install_python.sh
cd $VAGRANTDIR && source ./install_setuptools.sh
cd $VAGRANTDIR && source ./install_py2exe.sh
cd $VAGRANTDIR && source ./install_wine_wrappers.sh

cd $VAGRANTDIR && source ./install_dlfcn.sh
cd $VAGRANTDIR && source ./install_mman.sh

cd $VAGRANTDIR && source ./install_regex2dfa.sh
cd $VAGRANTDIR && source ./install_gmp.sh
cd $VAGRANTDIR && source ./install_pycrypto.sh
cd $VAGRANTDIR && source ./install_fte.sh
cd $VAGRANTDIR && source ./install_marionette.sh

cd $VAGRANTDIR && source ./package_marionette.sh
