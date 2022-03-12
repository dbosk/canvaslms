NOWEAVEFLAGS.tex=	-n -delay -t2
NOTANGLEFLAGS.py=

LATEXFLAGS+=	-shell-escape
TEX_PYTHONTEX=	yes

SRC_DIR=			../src/canvaslms

.PHONY: all
all: canvaslms.pdf

canvaslms.pdf: canvaslms.bib
canvaslms.pdf: abstract.tex
canvaslms.pdf: canvaslms.tex 

canvaslms.pdf: ${SRC_DIR}/hacks/canvasapi.tex
canvaslms.pdf: ${SRC_DIR}/cli/cli.tex
canvaslms.pdf: ${SRC_DIR}/cli/login.tex
canvaslms.pdf: ${SRC_DIR}/cli/courses.tex
canvaslms.pdf: ${SRC_DIR}/cli/users.tex
canvaslms.pdf: ${SRC_DIR}/cli/assignments.tex
canvaslms.pdf: ${SRC_DIR}/cli/submissions.tex
canvaslms.pdf: ${SRC_DIR}/cli/grade.tex
canvaslms.pdf: ${SRC_DIR}/cli/results.tex
canvaslms.pdf: ${SRC_DIR}/grades/grades.tex

${SRC_DIR}/%.tex: ${SRC_DIR}/%.nw
	${MAKE} -C $(dir $@) $(notdir $@)


.PHONY: clean
clean:
	${RM} canvaslms.pdf

.PHONY: distclean
distclean: clean
	${MAKE} -C ${SRC_DIR} clean distclean


INCLUDE_MAKEFILES=../makefiles
include ${INCLUDE_MAKEFILES}/tex.mk
include ${INCLUDE_MAKEFILES}/noweb.mk

