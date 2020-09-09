NOTANGLEFLAGS.py=


.PHONY: all
all: courses.pdf

courses.pdf: courses.nw
	${NOWEAVE.pdf}


.PHONY:
all: courses

courses.py: courses.nw
courses: courses.py
	cp $^ $@
	chmod +x $@


.PHONY: clean
clean:
	${RM} courses courses.py courses.pdf courses.tex


PKG_PACKAGES= 				courses

PKG_NAME-courses= 			courses
PKG_INSTALL_FILES-courses= 	courses
PKG_PREFIX-courses= 		/usr/local
PKG_INSTALL_DIR-courses= 	/bin
PKG_TARBALL_FILES-courses= 	${PKG_FILES-courses} Makefile


INCLUDE_MAKEFILES=../../makefiles
include ${INCLUDE_MAKEFILES}/tex.mk
include ${INCLUDE_MAKEFILES}/noweb.mk
include ${INCLUDE_MAKEFILES}/pkg.mk

