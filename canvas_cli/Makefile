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


.PHONY: clean
clean:
	${RM} canvas canvas.py canvas.pdf canvas.tex
	${RM} courses.tex users.tex



PKG_NAME-main= 			canvas
PKG_FILES-main= 		canvas
PKG_PREFIX-main= 		/usr/local
PKG_DIR-main= 			/bin
PKG_TARBALL_FILES-main= ${PKG_FILES-main} Makefile


INCLUDE_MAKEFILES=../makefiles
include ${INCLUDE_MAKEFILES}/tex.mk
include ${INCLUDE_MAKEFILES}/noweb.mk
include ${INCLUDE_MAKEFILES}/pkg.mk
