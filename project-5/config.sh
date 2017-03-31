apt-get -qqy update
apt-get -qqy install python-pip
pip install -r /vagrant/requirements.txt

vagrantTip="[35m[1mThe shared directory is located at /vagrant\nTo access your shared files: cd /vagrant(B[m"
echo -e $vagrantTip > /etc/motd
