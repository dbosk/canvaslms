NOTANGLEFLAGS.py=

MODULES+=	__init__.py cli.tex
MODULES+=	login.py login.tex
MODULES+=	courses.py courses.tex
MODULES+=	modules.py modules.tex
MODULES+=	users.py users.tex
MODULES+=	assignments.py assignments.tex
MODULES+=	submissions.py submissions.tex
MODULES+=	grade.py grade.tex
MODULES+=	results.py results.tex
MODULES+=	calendar.py calendar.tex
MODULES+=	discussions.py discussions.tex
MODULES+= 	utils.py utils.tex
MODULES+=	quizzes.py quizzes.tex
MODULES+=	cache.py cache.tex
MODULES+=	content.py content.tex
MODULES+=	pages.py pages.tex

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

