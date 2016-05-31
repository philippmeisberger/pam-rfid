PAM RFID
===============

PAM RFID is a Linux Pluggable Authentication Module (PAM) for RFID authentication. It uses the RDM6300 RFID reader in conjunction with the PyRfid library <https://github.com/philippmeisberger/pyrfid>.

Installation
------------

Add PM Codeworks repository

    ~# wget http://apt.pm-codeworks.de/pm-codeworks.list -P /etc/apt/sources.d/

Add PM Codeworks key

    ~# wget -O - http://apt.pm-codeworks.de/pm-codeworks.de.gpg.key | apt-key add -
    ~# apt-get update

Install the packages

    ~# apt-get install python-rfid libpam-rfid

Add group "dialout" for each user which should be able to use pamfingerprint

    ~# usermod -a -G dialout <username>
    ~# reboot

Setup
-----

Enable PAM RFID for a user

    ~# pamrfid-conf --add-user <username>

Test if everything works well

    ~# pamrfid-check --check-user <username>

Questions and suggestions
-------------------------

If you have any questions to this project just ask me via email:

<team@pm-codeworks.de>