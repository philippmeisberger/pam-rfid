PAM RFID
========

PAM RFID is a Linux Pluggable Authentication Module (PAM) for RFID authentication. It uses an EM4100 compatible RFID reader (e.g. RDM6300) in conjunction with the PyRfid library <https://github.com/philippmeisberger/pyrfid>.

Per default the password authentication is set as fallback in case no RFID sensor is connected. Two-factor authentication is also possible. The module has to be configured by the `pamrfid-conf` program.

Installation
------------

There are two ways of installing PAM RFID: Installation of the stable or latest version. The stable version is distributed through the PM Code Works APT repository and is fully tested but does not contain the latest changes.

### Installation of the stable version

Add PM Code Works repository

* Debian 8:

    `~# echo "deb http://apt.pm-codeworks.de jessie main" | tee /etc/apt/sources.list.d/pm-codeworks.list`

* Debian 9:

    `~# echo "deb http://apt.pm-codeworks.de stretch main" | tee /etc/apt/sources.list.d/pm-codeworks.list`

Add PM Code Works key

    ~# wget -qO - http://apt.pm-codeworks.de/pm-codeworks.de.gpg | apt-key add -
    ~# apt-get update

Install the packages

    ~# apt-get install python-rfid libpam-rfid

### Installation of the latest version

The latest version contains the latest changes that may not have been fully tested and should therefore not be used in production. It is recommended to install the stable version.

Install required packages for building

    ~# apt-get install git devscripts equivs

Clone this repository

    ~$ git clone https://github.com/philippmeisberger/pam-rfid.git

Build the package

    ~$ cd ./pam-rfid/src/
    ~$ sudo mk-build-deps -i debian/control
    ~$ dpkg-buildpackage -uc -us

Install the package

    ~# dpkg -i ../libpam-rfid*.deb

Install missing dependencies

    ~# apt-get install -f

Setup
-----

Add group "dialout" for each user which should be able to use PAM RFID

    ~# usermod -a -G dialout <username>
    ~# reboot

Enable PAM RFID for a user

    ~# pamrfid-conf --add-user <username>

Test if everything works well

    ~# pamrfid-conf --check-user <username>

Questions and suggestions
-------------------------

If you have any questions to this project just ask me via email:

<team@pm-codeworks.de>
