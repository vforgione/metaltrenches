# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  vagrant_version = Vagrant::VERSION.sub(/^v/, '')
  config.vm.box = "ubuntu/trusty64"
  config.vm.hostname = "metaltrenches"

  config.vm.provider :virtualbox do |v, override|
    v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
    v.customize ["modifyvm", :id, "--natdnsproxy1", "on"]
  end

  config.vm.network "private_network", type: :dhcp
  config.vm.network :forwarded_port, guest: 80, host: 4000
  config.vm.synced_folder ".", "/www/metaltrenches", owner: "www-data", group: "www-data", mount_options: ["dmode=755,fmode=755"]

  config.vm.provision :ansible do |ansible|
    ansible.playbook = "ansible/vagrant.yml"
  end

  config.vm.provider "virtualbox" do |v|
      v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
      v.customize ["modifyvm", :id, "--natdnsproxy1", "on"]
  end
end
