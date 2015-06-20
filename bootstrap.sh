#!/bin/bash

cd /vagrant
source ./setenv.sh
cd $VAGRANTDIR && python build_marionette.py
cd $VAGRANTDIR && python package_marionette.py
