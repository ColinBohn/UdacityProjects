# Linux Server Configuration
#### Information
* IP: 138.197.207.40
* SSH: 2200
* URL: [Recent Items - Catalog](http://138.197.207.40)

#### Actions Summary
* Configured and enabled UFW
	* [UncomplicatedFirewall - Ubuntu Wiki](https://wiki.ubuntu.com/UncomplicatedFirewall)
	* Ports allowed: 80, 123, 2200
* Created `grader` account and setup sudo, SSH
	* [How To Create a Sudo User on Ubuntu Quickstart | DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-create-a-sudo-user-on-ubuntu-quickstart)
	* [command line - Execute sudo without Password? - Ask Ubuntu](https://askubuntu.com/a/147265)
* Set timezone to UTC
* Installed nginx and configured UWSGI
	* [How to Deploy Python WSGI Applications Using uWSGI Web Server with Nginx | DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-deploy-python-wsgi-applications-using-uwsgi-web-server-with-nginx)
* Installed and configured PostgreSQL for catalog
	* [How To Install and Use PostgreSQL on Ubuntu 16.04 | DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-16-04)
	* [How To Secure PostgreSQL on an Ubuntu VPS | DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-secure-postgresql-on-an-ubuntu-vps)
* Cloned app and configured for SQLAlchemy for PostgreSQL
	* [Engine Configuration — SQLAlchemy 1.2 Documentation](http://docs.sqlalchemy.org/en/latest/core/engines.html)
