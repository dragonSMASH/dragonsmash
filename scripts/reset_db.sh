#!/usr/bin/env bash

MANAGE_PY="/home/vagrant/dragonsmash/manage.py"

confirm() {
    message=`echo -e $1`
    read -r -p "$message  " response

    if [[ ${response} =~ [yY][eE][sS]|[yY]$ ]]
    then
        return 0 # means true, a.k.a. go ahead, action confirmed
    else
        return 1
    fi
}

reset_db() {
    # remove and re-add the database
    sudo -u postgres psql -c "DROP DATABASE IF EXISTS dragonsmash;"
    sudo -u postgres createdb -O dsmash dragonsmash
    sudo -u postgres psql dragonsmash -c "CREATE EXTENSION postgis";

}

run_migrations() {
    ${MANAGE_PY} makemigrations
    ${MANAGE_PY} migrate
}

main() {
    echo -e "\nThis script will reset the database: completely drop it and then recreate it.\n\nThis is the NUCLEAR OPTION.\n"
    confirm "Are you sure you want to do this? [y/N]" &&
    confirm "Are you REALLY REALLY sure? [y/N]" &&
    echo -e "\nNo going back now. Hang on to your knickers: Here we go, nuking the database.\n" &&
    reset_db &&
    echo -e "\nDone! You're all set now champ, go wreak some havoc on your shiny new db."

    confirm "\nBut before you go, want me to create all the tables? [y/N]" && run_migrations
}

main
