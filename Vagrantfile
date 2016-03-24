# coding: utf-8
# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|

  config.vm.box = "ubuntu-14.04"
  config.vm.network "private_network", ip: "192.168.33.130"

  # Ansible
  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "./setup.yml"
    ansible.inventory_path = "./hosts"
    ansible.limit = "Docker-server"
  end
end
