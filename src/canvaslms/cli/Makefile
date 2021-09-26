NOWEAVEFLAGS.tex=	-n -delay -t2
NOTANGLEFLAGS.py=


.PHONY: all
all: __init__.py cli.tex
all: courses.py courses.tex
all: users.py users.tex
all: assignments.py assignments.tex
all: submissions.py submissions.tex
all: grade.py grade.tex

__init__.py: cli.py
	mv $< $@


.PHONY: clean
clean:
	${RM} cli.tex cli.py __init__.py
	${RM} courses.tex courses.py
	${RM} users.tex users.py
	${RM} assignments.tex assignments.py
	${RM} submissions.tex submissions.py
	${RM} grade.tex grade.py


INCLUDE_MAKEFILES=../../../makefiles
include ${INCLUDE_MAKEFILES}/tex.mk
include ${INCLUDE_MAKEFILES}/noweb.mk
include ${INCLUDE_MAKEFILES}/pkg.mk

