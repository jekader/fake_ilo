bindir=$(DESTDIR)/usr/bin
sysconfdir=$(DESTDIR)/etc

all:
#	openssl req -x509 -newkey rsa:2048 -keyout $(sysconfdir)/server.key -out $(sysconfdir)/server.crt -nodes -days 9999 -subj "/C=MD/ST=Chisinau/L=Chisinau/O=IT/CN=www.example.com"
	openssl req -x509 -newkey rsa:2048 -keyout server.key -out server.crt -nodes -days 9999 -subj "/C=MD/ST=Chisinau/L=Chisinau/O=IT/CN=www.example.com"
	echo "Nothing to compile, please run make install"
install: all
#	env
	mkdir -p $(sysconfdir)/fake_ilo/
	install -m 0755 ilo.py $(bindir)
	install -m 0755 fake_ilo $(sysconfdir)/init.d/
	install -m 0600 server.key $(sysconfdir)/fake_ilo/
	install -m 0600 server.crt $(sysconfdir)/fake_ilo/

clean:
	rm -f server.key
	rm -f server.crt
