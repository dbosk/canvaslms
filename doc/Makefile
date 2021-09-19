NOWEAVEFLAGS.tex=	-n -delay -t2
NOTANGLEFLAGS.py=

SRC_DIR=			../src/canvaslmscli

.PHONY: all
all: canvas.pdf

canvas.pdf: canvas.bib
canvas.pdf: abstract.tex

canvas.pdf: canvas.tex 
canvas.tex: ${SRC_DIR}/canvas.nw

canvas.pdf: courses.tex
courses.tex: ${SRC_DIR}/courses.nw

canvas.pdf: course.tex
course.tex: ${SRC_DIR}/course.nw

canvas.pdf: users.tex
users.tex: ${SRC_DIR}/users.nw

canvas.pdf: assignments.tex
assignments.tex: ${SRC_DIR}/assignments.nw

canvas.pdf: submissions.tex
submissions.tex: ${SRC_DIR}/submissions.nw

canvas.pdf: grades.tex
grades.tex: ${SRC_DIR}/grades.nw

%.tex: ${SRC_DIR}/%.nw
	${NOWEAVE.tex}


.PHONY: clean
clean:
	${RM} canvas.pdf canvas.tex
	${RM} courses.tex course.tex users.tex assignments.tex
	${RM} submissions.tex grades.tex


INCLUDE_MAKEFILES=../makefiles
include ${INCLUDE_MAKEFILES}/tex.mk
include ${INCLUDE_MAKEFILES}/noweb.mk

