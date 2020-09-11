NOWEAVEFLAGS.tex=	-n -delay -t2
NOTANGLEFLAGS.py=


.PHONY: all
all: canvas.pdf canvas

canvas.pdf: canvas.tex canvas.bib
canvas.pdf: abstract.tex

canvas.tex: canvas.nw

canvas.py: canvas.nw
canvas: canvas.py
	cp $^ $@
	chmod +x $@


canvas.pdf: courses.tex
canvas.py: courses.nw

canvas.pdf: users.tex
canvas.py: users.nw

canvas.pdf: assignments.tex
canvas.py: assignments.nw

canvas.pdf: submissions.tex
canvas.py: submissions.nw


.PHONY: all
all: canvas.bash

canvas.bash: canvas
	register-python-argcomplete canvas > $@


.PHONY: clean
clean:
	${RM} canvas canvas.py canvas.pdf canvas.tex
	${RM} courses.tex users.tex
	${RM} canvas.bash


PKG_PACKAGES= 					canvas canvas.bash

PKG_NAME-canvas= 				canvas
PKG_INSTALL_FILES-canvas=		canvas
PKG_PREFIX-canvas= 				/usr/local
PKG_INSTALL_DIR-canvas=			/bin
PKG_TARBALL_FILES-canvas= 		${PKG_INSTALL_FILES-canvas} Makefile

PKG_NAME-canvas.bash=			canvas.bash
PKG_INSTALL_FILES-canvas.bash=	canvas.bash
PKG_PREFIX-canvas.bash=			
PKG_INSTALL_DIR-canvas.bash=	/etc/bash_completion.d
PKG_TARBALL_FILES-canvas.bash=	${PKG_INSTALL_FILES-canvas.bash} Makefile


INCLUDE_MAKEFILES=../makefiles
include ${INCLUDE_MAKEFILES}/tex.mk
include ${INCLUDE_MAKEFILES}/noweb.mk
include ${INCLUDE_MAKEFILES}/pkg.mk

