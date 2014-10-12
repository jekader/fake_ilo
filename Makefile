all:
	echo "Nothing to compile, please run make install"
install:
	mkdir -p /etc/fake_ilo/
	openssl req -x509 -newkey rsa:2048 -keyout /etc/fake_ilo/server.key -out /etc/fake_ilo/server.crt -nodes -days 9999 -subj "/C=MD/ST=Chisinau/L=Chisinau/O=IT/CN=www.example.com"
	cp ilo.py /usr/local/bin/
