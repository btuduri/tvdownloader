.PHONY : build install clean

# Repertoires
PREFIX ?= /usr
BINDIR ?= $(PREFIX)/bin
DATADIR ?= $(PREFIX)/share

# Commande pour l'installation
INSTALL = install -m 755


# Compilation
build : 
	# ByteCode
	@python -c "import compileall ; compileall.compile_dir( 'src' )"
	# On modifie le lanceur
	sed -i 's|__DATADIR__|$(DESTDIR)$(DATADIR)|g' tvdownloader.sh

# Installation
install :
	# On met en place le lanceur
	mkdir -p $(DESTDIR)$(BINDIR)
	$(INSTALL) tvdownloader.sh $(DESTDIR)$(BINDIR)/tvdownloader
	# On change les droits du fichier (il doit etre executable)
	chmod 0755 $(DESTDIR)$(BINDIR)/tvdownloader
	
	# On met en place le .desktop
	mkdir -p $(DESTDIR)$(DATADIR)/applications
	$(INSTALL) tvdownload.desktop $(DESTDIR)$(DATADIR)/applications/
	
	# On met en place l'icone
	mkdir -p $(DESTDIR)$(DATADIR)/pixmaps
	$(INSTALL) tvdownloader.png $(DESTDIR)$(DATADIR)/pixmaps/
	
	# On met en place la doc
	mkdir -p $(DESTDIR)$(DATADIR)/doc/tvdownloader
	cp -r doc/* $(DESTDIR)$(DATADIR)/doc/tvdownloader/
	# On change les droits
	chmod -R 0755 $(DESTDIR)$(DATADIR)/doc/tvdownloader
	
	# On met en place le code
	mkdir -p $(DESTDIR)$(DATADIR)/tvdownloader
	cp -r src/* $(DESTDIR)$(DATADIR)/tvdownloader/
	# On change les droits
	chmod -R 0755 $(DESTDIR)$(DATADIR)/tvdownloader

# Nettoyage
clean : 
	echo "Nothing"
	#~ @rm -vf {src,src/fonctions,src/GUI,src/GUI/Qt,src/ico,src/lib,src/plugins}/*{pyc,pyo,~}