NOTANGLEFLAGS.py=

LATEXFLAGS+=	-shell-escape
TEX_PYTHONTEX=	yes

SRC_DIR=			../src/canvaslms
TEST_DIR=			../tests

# Example scripts tangled from intro.nw
EXAMPLES+=	examples/explore-courses.sh
EXAMPLES+=	examples/list-ungraded.sh
EXAMPLES+=	examples/grade-ssh-login.sh
EXAMPLES+=	examples/export-page.sh
EXAMPLES+=	examples/import-page.sh
EXAMPLES+=	examples/analyse-survey.sh
EXAMPLES+=	examples/export-ladok.sh
EXAMPLES+=	examples/update-dates.sh

.PHONY: all
all: canvaslms.pdf

canvaslms.pdf: canvaslms.bib
canvaslms.pdf: abstract.tex
canvaslms.pdf: canvaslms.tex
canvaslms.pdf: didactic.sty
canvaslms.pdf: intro.tex
canvaslms.pdf: ${EXAMPLES}

canvaslms.pdf: ${SRC_DIR}/hacks/canvasapi.tex
canvaslms.pdf: ${SRC_DIR}/hacks/attachment_cache.tex
canvaslms.pdf: ${SRC_DIR}/cli/cli.tex
canvaslms.pdf: ${SRC_DIR}/cli/login.tex
canvaslms.pdf: ${SRC_DIR}/cli/courses.tex
canvaslms.pdf: ${SRC_DIR}/cli/users.tex
canvaslms.pdf: ${SRC_DIR}/cli/utils.tex
canvaslms.pdf: ${SRC_DIR}/cli/assignments.tex
canvaslms.pdf: ${SRC_DIR}/cli/submissions.tex
canvaslms.pdf: ${SRC_DIR}/cli/modules.tex
canvaslms.pdf: ${SRC_DIR}/cli/grade.tex
canvaslms.pdf: ${SRC_DIR}/cli/results.tex
canvaslms.pdf: ${SRC_DIR}/grades/grades.tex
canvaslms.pdf: ${SRC_DIR}/cli/calendar.tex
canvaslms.pdf: ${SRC_DIR}/cli/discussions.tex
canvaslms.pdf: ${SRC_DIR}/cli/quizzes.tex
canvaslms.pdf: ${TEST_DIR}/conftest.tex

canvaslms.pdf: src

.PHONY: src
src:
	${MAKE} -C ${SRC_DIR} all

${SRC_DIR}/%.tex: ${SRC_DIR}/%.nw
	${MAKE} -C $(dir $@) $(notdir $@)

# Introduction chapter
intro.tex: intro.nw

# Example scripts - tangled from intro.nw
examples:
	mkdir -p examples

${EXAMPLES}: intro.nw | examples
	notangle -R"$@" $< > $@
	chmod +x $@


.PHONY: clean
clean:
	${RM} canvaslms.pdf
	${RM} intro.tex
	${RM} -r examples

.PHONY: distclean
distclean: clean
	${MAKE} -C ${SRC_DIR} clean distclean
	${MAKE} -C ${TEST_DIR} clean distclean


INCLUDE_MAKEFILES=../makefiles
include ${INCLUDE_MAKEFILES}/tex.mk
include ${INCLUDE_MAKEFILES}/noweb.mk

INCLUDE_DIDACTIC=./didactic
include ${INCLUDE_DIDACTIC}/didactic.mk
