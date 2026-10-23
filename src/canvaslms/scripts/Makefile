MODULES+=	ungraded.sh ungraded.tex

.PHONY: all
all: ${MODULES}

# cron runs the installed copy directly, so it must be executable.
ungraded.sh: ungraded.nw
	${NOTANGLE.sh}
	chmod 755 $@


.PHONY: clean
clean:
	${RM} ${MODULES}

.PHONY: distclean
distclean:
	${RM} -Rf ltxobj


INCLUDE_MAKEFILES=../../../makefiles
include ${INCLUDE_MAKEFILES}/tex.mk
include ${INCLUDE_MAKEFILES}/noweb.mk
