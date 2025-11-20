# Makefile for canvaslms test suite
#
# Tests are written in .nw files throughout the src/ tree using
# chunks named "<<test modulename.py>>". This Makefile extracts
# those test chunks and tangles them to tests/unit/test_*.py files.

# Explicitly list test modules we expect
# (As we add test chunks to .nw files, add corresponding test_*.py here)
TEST_MODULES+=	conftest.py
TEST_MODULES+=	unit/test_utils.py
TEST_MODULES+=	unit/test_courses.py
TEST_MODULES+=	unit/test_hacks.py

# Also generate .tex for documentation
DOC_MODULES+=	conftest.tex

.PHONY: all
all: ${TEST_MODULES} ${DOC_MODULES}

# conftest.py is tangled from tests/conftest.nw
conftest.py: conftest.nw
	notangle -R$(notdir $@) $< | cpif $@ && noroots $<

conftest.tex: conftest.nw
	noweave -x -n -delay -t2 $< > $@

# Test files are extracted from their source .nw files
# Note: chunk names have spaces: "<<test utils.py>>" not "<<test_utils.py>>"

unit/test_utils.py: ../src/canvaslms/cli/utils.nw
	notangle -R"test utils.py" $< | cpif $@ && noroots $<

unit/test_courses.py: ../src/canvaslms/cli/courses.nw
	notangle -R"test courses.py" $< | cpif $@ && noroots $<

unit/test_hacks.py: ../src/canvaslms/hacks/canvasapi.nw
	notangle -R"test hacks.py" $< | cpif $@ && noroots $<

# Target to run tests after tangling
.PHONY: test
test: all
	poetry run pytest -v --cov=canvaslms --cov-report=term-missing

# Clean generated test files
.PHONY: clean
clean:
	${RM} ${TEST_MODULES} ${DOC_MODULES}
	${RM} -r .pytest_cache __pycache__ unit/__pycache__
	${RM} -r htmlcov .coverage

INCLUDE_MAKEFILES=../makefiles
include ${INCLUDE_MAKEFILES}/tex.mk
