LIBDIR = $(DESTDIR)/usr/lib/pamrfid
BINDIR = $(DESTDIR)/usr/bin

clean:
	rm -f *.py[co] */*.py[co]

install:
	mkdir -p $(LIBDIR)
	cp -r src/etc/ $(DESTDIR)/
	cp -r src/lib/ $(DESTDIR)/
	cp -r src/usr/ $(DESTDIR)/

uninstall:
	rm -rf $(LIBDIR)
	rm -f $(DESTDIR)/usr/share/pam-configs/rfid
	rm -f $(BINDIR)/pamrfid-check
	rm -f $(BINDIR)/pamrfid-conf
	rm -f $(DESTDIR)/lib/security/pam_rfid.py
	rm -f $(DESTDIR)/etc/bash_completion.d/pamrfid
	rm -f $(DESTDIR)/etc/pamrfid.conf
