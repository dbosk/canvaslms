NOWEAVEFLAGS.tex=	-n -delay -t2
NOTANGLEFLAGS.py=

MODULES+=	__init__.py cli.tex
MODULES+=	login.py login.tex
MODULES+=	courses.py courses.tex
MODULES+=	users.py users.tex
MODULES+=	assignments.py assignments.tex
MODULES+=	submissions.py submissions.tex
MODULES+=	grade.py grade.tex
MODULES+=	results.py results.tex

.PHONY: all
all: ${MODULES}

.INTERMEDIATE: cli.py
__init__.py: cli.py
	mv $< $@


.PHONY: clean
clean:
	${RM} ${MODULES}


INCLUDE_MAKEFILES=../../../makefiles
include ${INCLUDE_MAKEFILES}/tex.mk
include ${INCLUDE_MAKEFILES}/noweb.mk
include ${INCLUDE_MAKEFILES}/pkg.mk

