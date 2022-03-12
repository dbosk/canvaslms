NOWEAVEFLAGS.tex=	-n -delay -t2
NOTANGLEFLAGS.py=


.PHONY: all
all: grades.tex
all: conjunctavg.py conjunctavg.tex
all: disjunctmax.py disjunctmax.tex

grades.tex: conjunctavg.tex
grades.tex: disjunctmax.tex


.PHONY: clean
clean:
	${RM} grades.tex
	${RM} conjunctavg.py conjunctavg.tex
	${RM} disjunctmax.py disjunctmax.tex


INCLUDE_MAKEFILES=../../../makefiles
include ${INCLUDE_MAKEFILES}/tex.mk
include ${INCLUDE_MAKEFILES}/noweb.mk
include ${INCLUDE_MAKEFILES}/pkg.mk

