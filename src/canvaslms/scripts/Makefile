MODULES+=	ungraded.sh ungraded.tex
MODULES+=	carryover.sh carryover.tex

.PHONY: all
all: ${MODULES}

# The scripts are run as installed, by cron among others, so they must be
# executable.
ungraded.sh carryover.sh: %.sh: %.nw
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
