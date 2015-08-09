# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty64"

  config.vm.network "forwarded_port", guest: 8000, host: 8000

  # disable the default synced folder
  config.vm.synced_folder ".", "/vagrant", disabled: true
  # sync django source to home directory of vagrant user
  config.vm.synced_folder "./dragonsmash", "/home/vagrant/dragonsmash", create: true

  config.vm.provision "shell", inline: <<-SHELL

    # updates package listing
    sudo apt-get update

    # base system upgrades
    sudo apt-get dist-upgrade -y
    sudo apt-get upgrade -y

    # python packages
    sudo apt-get install -y python3 python3-pip python3-dev

    # GIS packages
    sudo apt-get install -y binutils libproj-dev gdal-bin python-gdal

    # Postgres/PostGIS packages
    sudo apt-get install -y libpq-dev postgresql-9.3 postgresql-9.3-postgis-2.1 postgresql-server-dev-9.3 postgresql-contrib

    #cleanup
    sudo apt-get autoremove -y


    # set up live database
    sudo -u postgres createuser dsmash -S -D -R
    sudo -u postgres psql -c "ALTER ROLE dsmash WITH PASSWORD 'password';"
    sudo -u postgres createdb -O dsmash dragonsmash
    sudo -u postgres psql dragonsmash -c "CREATE EXTENSION postgis";

    # set up test database
    sudo -u postgres createuser test_dsmash -S -D -R
    sudo -u postgres psql -c "ALTER ROLE test_dsmash WITH PASSWORD 'password';"
    sudo -u postgres createdb -O test_dsmash test_dragonsmash
    sudo -u postgres psql test_dragonsmash -c "CREATE EXTENSION postgis";


    # set up python environment
    sudo pip3 install virtualenv --upgrade
    virtualenv -p python3 /home/vagrant/mistymountain
    source /home/vagrant/mistymountain/bin/activate
    pip3 install -r /home/vagrant/dragonsmash/requirements/dev.txt --upgrade

    # install models to db
    /home/vagrant/dragonsmash/manage.py makemigrations api # TODO: can this be removed once migrations are committed in?
    /home/vagrant/dragonsmash/manage.py migrate


    # set up convenience bashrc
    echo "source /home/vagrant/mistymountain/bin/activate" > /home/vagrant/.bashrc
    echo "cd dragonsmash" >> /home/vagrant/.bashrc

  SHELL
end
