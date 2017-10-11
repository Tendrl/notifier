NAME=pyasn1
VERSION := 0.3.7
RELEASE=1
COMMIT := $(shell git rev-parse HEAD)
SHORTCOMMIT := $(shell echo $(COMMIT) | cut -c1-7)

all: srpm

clean:
	rm -fr pyasn1 python2-pyasn1-$(VERSION)
	rm -rf dist/
	rm -rf $(NAME)-$(VERSION).tar.gz
	rm -rf $(NAME)-$(VERSION)-$(RELEASE).el7.src.rpm

dist:
	git clone https://github.com/etingof/pyasn1
	mv pyasn1 python2-$(NAME)-$(VERSION)
	cp -r python-pyasn1.spec  python2-$(NAME)-$(VERSION)/
	tar -zcf $(NAME)-$(VERSION).tar.gz python2-$(NAME)-$(VERSION)
	rm -rf python2-$(NAME)-$(VERSION)

srpm: dist
	fedpkg --dist epel7 srpm

rpm: dist
	mock -r epel-7-x86_64 rebuild python2-$(NAME)-$(VERSION)-*.src.rpm --resultdir=. --define "dist .el7"


.PHONY: dist rpm srpm
