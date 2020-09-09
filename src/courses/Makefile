.PHONY: all
all: courses.pdf

NOWEAVEFLAGS.tex=	-x -t2
NOTANGLEFLAGS.py=

courses.pdf: courses.tex

courses.tex: courses.nw


.PHONY:
all: courses

courses.py: courses.nw
courses: courses.py
	cp $^ $@
	chmod +x $@


.PHONY: clean
clean:
	${RM} courses courses.py courses.pdf courses.tex


PKG_NAME-main= 			courses
PKG_INSTALL_FILES-main= courses
PKG_PREFIX-main= 		/usr/local
PKG_INSTALL_DIR-main= 	/bin
PKG_TARBALL_FILES-main= ${PKG_FILES-main} Makefile


INCLUDE_MAKEFILES=../../makefiles
include ${INCLUDE_MAKEFILES}/tex.mk
include ${INCLUDE_MAKEFILES}/noweb.mk
include ${INCLUDE_MAKEFILES}/pkg.mk

