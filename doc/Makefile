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

# The minted code blocks are highlighted with noweb's custom Pygments lexer,
# which noweb.mk copies in from the noweb library (see its noweb_lexer.py rule).
canvaslms.pdf: noweb_lexer.py

canvaslms.pdf: ${SRC_DIR}/hacks/canvasapi.tex
canvaslms.pdf: ${SRC_DIR}/hacks/attachment_cache.tex
canvaslms.pdf: ${SRC_DIR}/canvaslms.tex
canvaslms.pdf: ${SRC_DIR}/cli/cli.tex
canvaslms.pdf: ${SRC_DIR}/cli/login.tex
canvaslms.pdf: ${SRC_DIR}/cli/courses.tex
canvaslms.pdf: ${SRC_DIR}/cli/users.tex
canvaslms.pdf: ${SRC_DIR}/cli/utils.tex
canvaslms.pdf: ${SRC_DIR}/cli/content.tex
canvaslms.pdf: ${SRC_DIR}/cli/assignments.tex
canvaslms.pdf: ${SRC_DIR}/cli/submissions.tex
canvaslms.pdf: ${SRC_DIR}/cli/modules.tex
canvaslms.pdf: ${SRC_DIR}/cli/pages.tex
canvaslms.pdf: ${SRC_DIR}/cli/syllabus.tex
canvaslms.pdf: ${SRC_DIR}/cli/grade.tex
canvaslms.pdf: ${SRC_DIR}/cli/results.tex
canvaslms.pdf: ${SRC_DIR}/grades/grades.tex
canvaslms.pdf: ${SRC_DIR}/cli/calendar.tex
canvaslms.pdf: ${SRC_DIR}/cli/discussions.tex
canvaslms.pdf: ${SRC_DIR}/cli/quizzes.tex
canvaslms.pdf: ${SRC_DIR}/cli/cache.tex
canvaslms.pdf: ${TEST_DIR}/conftest.tex
canvaslms.pdf: lint.tex

canvaslms.pdf: src

.PHONY: src
src:
	${MAKE} -C ${SRC_DIR} all

../%:
	${MAKE} -C $(dir $@) $(notdir $@)

# Introduction chapter
intro.tex: intro.nw

# Cross-reference lint - both the chapter and the script it explains.
# `make lint` audits the sources; the same audit also runs as a unit test.
lint.tex: lint.nw
lint.py: lint.nw

.PHONY: lint
lint: lint.py
	python3 lint.py

# Example scripts - tangled from intro.nw
examples:
	mkdir -p examples

${EXAMPLES}: intro.nw | examples
	notangle -R"[[$@]]" $< > $@
	chmod +x $@


.PHONY: clean
clean:
	${RM} canvaslms.pdf
	${RM} intro.tex
	${RM} lint.tex lint.py
	${RM} -r examples
	${RM} -r __pycache__

.PHONY: distclean
distclean: clean
	${MAKE} -C ${SRC_DIR} clean distclean
	${MAKE} -C ${TEST_DIR} clean distclean


INCLUDE_MAKEFILES=../makefiles
include ${INCLUDE_MAKEFILES}/tex.mk
include ${INCLUDE_MAKEFILES}/noweb.mk

INCLUDE_DIDACTIC=./didactic
include ${INCLUDE_DIDACTIC}/didactic.mk
