# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty64"

  config.vm.network "forwarded_port", guest: 8000, host: 8000

  # disable the default synced folder
  config.vm.synced_folder ".", "/vagrant", disabled: true
  # sync django source to home directory of vagrant user
  config.vm.synced_folder "./dragonsmash", "/home/vagrant/dragonsmash", create: true

  config.push.define "local-exec" do |push|
    push.inline = "echo 'deploying app...'"
  end

  config.vm.provision "ansible" do |ansible|
    ansible.groups = {
        "dev" => ["default"],
    }
    ansible.playbook = "provisioning/dev.yml"
  end

end
