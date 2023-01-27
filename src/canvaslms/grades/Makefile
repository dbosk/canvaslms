NOWEAVEFLAGS.tex=	-n -delay -t2
NOTANGLEFLAGS.py=

MODULES+=			conjunctavg.py
MODULES+=			disjunctmax.py
MODULES+=			maxgradesurvey.py
MODULES+=			conjunctavgsurvey.py

.PHONY: all
all: grades.tex
all: conjunctavg.py conjunctavg.tex
all: disjunctmax.py disjunctmax.tex
all: maxgradesurvey.py maxgradesurvey.tex
all: conjunctavgsurvey.py conjunctavgsurvey.tex

grades.tex: conjunctavg.tex
grades.tex: disjunctmax.tex
grades.tex: maxgradesurvey.tex
grades.tex: conjunctavgsurvey.tex


.PHONY: clean
clean:
	${RM} grades.tex
	${RM} ${MODULES}


INCLUDE_MAKEFILES=../../../makefiles
include ${INCLUDE_MAKEFILES}/tex.mk
include ${INCLUDE_MAKEFILES}/noweb.mk
include ${INCLUDE_MAKEFILES}/pkg.mk

