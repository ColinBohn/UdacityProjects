# Tournament DB

This project creates a PostgreSQL database structured to store a swiss-style tournament. It also provides a Python interface to easily query this database.

## Instructions

1. Download and install [VirtualBox](https://www.virtualbox.org/wiki/Downloads).
2. Download and install [Vagrant](https://www.vagrantup.com/downloads.html).
3. Download the [Udacity VM](https://github.com/udacity/fullstack-nanodegree-vm/) and launch `vagrant up`
4. Move the files from this project into `/vagrant/tournament`
5. Connect into the VM `vagrant ssh`
6. Connect to the PostgreSQL server `psql`
7. Create a new tournament database `create database tournament`
8. Change to the tournament database `\c tournament`
9. Import the table schemas `\i tournament.sql`
10. Quit out of PostgreSQL `\q`
11. Run test to check configuration `python tournament_test.py`