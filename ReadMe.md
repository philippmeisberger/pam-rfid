Install instructions for Debian 7
=================================

* Add PM Codeworks repository:
    * `~# wget http://apt.pm-codeworks.de/pm-codeworks.list -P /etc/apt/sources.d/`

* Add PM Codeworks key:
    * `~# wget -O - http://apt.pm-codeworks.de/pm-codeworks.de.gpg.key | apt-key add -`
    * `~# apt-get update`

* Install the package:
    * `~# apt-get install pamrfid`

* Add group "dialout" for each user which should be able to use pamrfid:
    * `~# usermod -a -G dialout <username>`
    * `~# reboot`

* Setup user
    * `~# pamrfid-conf --add-user <username>`
