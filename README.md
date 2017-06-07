PAM RFID
========

PAM RFID is a Linux Pluggable Authentication Module (PAM) for RFID authentication. It uses an EM4100 compatible RFID reader (e.g. RDM6300) in conjunction with the PyRfid library <https://github.com/philippmeisberger/pyrfid>.

Per default the password authentication is set as fallback in case no RFID sensor is connected. Two-factor authentication is also possible. The module has to be configured by the `pamrfid-conf` program. To simulate an authentication process the `pamrfid-check` program can be used.

Installation
------------

There are two ways of installing PAM RFID: Installation of the stable or latest version. The stable version is distributed through the PM Code Works APT repository and is fully tested but does not contain the latest changes.

### Installation of the stable version

Add PM Codeworks repository

    ~# wget http://apt.pm-codeworks.de/pm-codeworks.list -P /etc/apt/sources.d/

Add PM Codeworks key

    ~# wget -O - http://apt.pm-codeworks.de/pm-codeworks.de.gpg | apt-key add -
    ~# apt-get update

Install the packages

    ~# apt-get install python-rfid libpam-rfid

### Installation of the latest version

The latest version contains the latest changes that may not have been fully tested and should therefore not be used productively. It is recommended to install the stable version.

Install required packages for building

    ~# apt-get install git devscripts

Clone this repository

    ~$ git clone https://github.com/philippmeisberger/pam-rfid.git

Build the package

    ~$ cd ./pam-rfid/
    ~$ dpkg-buildpackage -uc -us

Install the package

    ~# dpkg -i ../libpam-rfid*.deb

Setup
-----

Add group "dialout" for each user which should be able to use PAM RFID

    ~# usermod -a -G dialout <username>
    ~# reboot

Enable PAM RFID for a user

    ~# pamrfid-conf --add-user <username>

Test if everything works well

    ~# pamrfid-check --check-user <username>

Questions and suggestions
-------------------------

If you have any questions to this project just ask me via email:

<team@pm-codeworks.de>
