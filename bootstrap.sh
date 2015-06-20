#!/bin/bash

cd /vagrant
source ./setenv.sh

python build_marionette.py

cd $VAGRANTDIR && source ./package_marionette.sh
