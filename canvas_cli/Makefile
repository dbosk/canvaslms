NOTANGLEFLAGS.py=


.PHONY: all
all: courses.pdf courses

courses.pdf: courses.nw
	${NOWEAVE.pdf}

courses.py: courses.nw
courses: courses.py
	cp $^ $@
	chmod +x $@



.PHONY: all
all: users.pdf users

users.pdf: users.nw
	${NOWEAVE.pdf}

users.py: users.nw
users: users.py
	cp $^ $@
	chmod +x $@



.PHONY: clean
clean:
	${RM} courses courses.py courses.pdf courses.tex
	${RM} users users.py users.pdf users.tex



PKG_PACKAGES= 				courses users

PKG_NAME-courses= 			courses
PKG_INSTALL_FILES-courses= 	courses
PKG_PREFIX-courses= 		/usr/local
PKG_INSTALL_DIR-courses= 	/bin
PKG_TARBALL_FILES-courses= 	${PKG_INSTALL_FILES-courses} Makefile

PKG_NAME-users= 			users
PKG_INSTALL_FILES-users= 	users
PKG_PREFIX-users= 			/usr/local
PKG_INSTALL_DIR-users= 		/bin
PKG_TARBALL_FILES-users= 	${PKG_INSTALL_FILES-users} Makefile



INCLUDE_MAKEFILES=../makefiles
include ${INCLUDE_MAKEFILES}/tex.mk
include ${INCLUDE_MAKEFILES}/noweb.mk
include ${INCLUDE_MAKEFILES}/pkg.mk

