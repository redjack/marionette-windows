#!/bin/bash

cd /vagrant
source ./setenv.sh

python build_marionette.py

cd $VAGRANTDIR && source ./install_gmp.sh
cd $VAGRANTDIR && source ./install_pycrypto.sh
cd $VAGRANTDIR && source ./install_fte.sh
cd $VAGRANTDIR && source ./install_marionette.sh

cd $VAGRANTDIR && source ./package_marionette.sh
