# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/precise32"
  config.ssh.username = "vagrant"

  config.vm.provider "virtualbox" do |vb|
    vb.memory = "4096"
  end

#  config.vm.provision :shell, path: "bootstrap.sh", privileged: false
end
