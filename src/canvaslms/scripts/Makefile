.PHONY: all
all: oldresults.pdf

LATEXFLAGS+=	-shell-escape
NOWEAVEFLAGS+=	-option "shift,breakcode,longchunks,longxref"

.INTERMEDIATE: oldresults.tex
oldresults.pdf: oldresults.nw
	${NOWEAVE.pdf}


.PHONY:
all: oldresults

oldresults.sh: oldresults.nw
oldresults: oldresults.sh
	cp $^ $@
	chmod +x $@


.PHONY: clean
clean:
	${RM} oldresults oldresults.sh oldresults.pdf oldresults.tex
	${RM} oldresults.aux oldresults.fdb_latexmk oldresults.fls
	${RM} oldresults.log oldresults.out


INCLUDE_MAKEFILES=../../../makefiles
include ${INCLUDE_MAKEFILES}/tex.mk
include ${INCLUDE_MAKEFILES}/noweb.mk
