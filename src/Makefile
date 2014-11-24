LIBDIR = $(DESTDIR)/usr/lib/pamrfid
BINDIR = $(DESTDIR)/usr/bin

clean:
	rm -f *.py[co] */*.py[co]

install:
	mkdir -p $(LIBDIR)
	cp -r files/etc/ $(DESTDIR)/
	cp -r files/lib/ $(DESTDIR)/
	cp -r files/usr/ $(DESTDIR)/
	#pam-auth-update --package rfid

uninstall:
	#find /usr/lib/pamrfid/ -type f -name *.pyc -exec rm {} \;
	#pam-auth-update --package --remove rfid
	rm -f $(DESTDIR)/usr/share/pam-configs/rfid
	rm -f $(BINDIR)/pamrfid-check
	rm -f $(BINDIR)/pamrfid-conf
	rm -f $(DESTDIR)/lib/security/pam_rfid.py
	rm -f $(DESTDIR)/etc/bash_completion.d/pamrfid
	rm -f $(DESTDIR)/etc/pamrfid.conf
	rm -rf $(LIBDIR)
