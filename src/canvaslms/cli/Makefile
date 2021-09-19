NOWEAVEFLAGS.tex=	-n -delay -t2
NOTANGLEFLAGS.py=


.PHONY: all
all: assignments.py
all: cli.py
all: course.py
all: courses.py
all: grades.py
all: submissions.py
all: users.py


.PHONY: clean
clean:
	${RM} cli.tex cli.py
	${RM} courses.tex courses.py
	${RM} course.tex course.py
	${RM} users.tex users.py
	${RM} assignments.tex assignments.py
	${RM} submissions.tex submissions.py
	${RM} grades.tex grades.py


INCLUDE_MAKEFILES=../../../makefiles
include ${INCLUDE_MAKEFILES}/tex.mk
include ${INCLUDE_MAKEFILES}/noweb.mk
include ${INCLUDE_MAKEFILES}/pkg.mk

