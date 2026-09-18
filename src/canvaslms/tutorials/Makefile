NOWEB_SUFFIXES+=	.md

MODULES+=	getting-started.md getting-started.tex
MODULES+=	assignments-and-grading.md assignments-and-grading.tex

.PHONY: all
all: ${MODULES}

getting-started.md: getting-started.nw
assignments-and-grading.md: assignments-and-grading.nw


.PHONY: clean
clean:
	${RM} ${MODULES}

.PHONY: distclean
distclean:
	${RM} -Rf ltxobj


INCLUDE_MAKEFILES=../../../makefiles
include ${INCLUDE_MAKEFILES}/tex.mk
include ${INCLUDE_MAKEFILES}/noweb.mk
