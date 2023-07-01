NOTANGLEFLAGS.py=

MODULES+=			__init__.py
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
all: ${MODULES}

grades.tex: conjunctavg.tex
grades.tex: disjunctmax.tex
grades.tex: maxgradesurvey.tex
grades.tex: conjunctavgsurvey.tex

__init__.py: init.py
	${MV} $^ $@

.INTERMEDIATE: init.py
init.py: grades.nw
	${NOTANGLE.py}


.PHONY: clean
clean:
	${RM} grades.tex
	${RM} ${MODULES}
	${RM} init.py


INCLUDE_MAKEFILES=../../../makefiles
include ${INCLUDE_MAKEFILES}/tex.mk
include ${INCLUDE_MAKEFILES}/noweb.mk
include ${INCLUDE_MAKEFILES}/pkg.mk

