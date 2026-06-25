SUBDIR_GOALS=	all clean distclean

SUBDIR+=		src/canvaslms
SUBDIR+=		doc
SUBDIR+=		docker
SUBDIR+=		tests

version=$(shell sed -n 's/^ *version *= *\"\([^\"]\+\)\"/\1/p' pyproject.toml)


.PHONY: all
all: compile doc/canvaslms.pdf test

.PHONY: test
test:
	${MAKE} -C tests test

.PHONY: install
install: compile
	python3 -m pip install -e .
	register-python-argcomplete canvaslms > canvaslms.bash
	sudo install canvaslms.bash /etc/bash_completion.d/
	rm canvaslms.bash

.PHONY: compile
compile:
	${MAKE} -C src/canvaslms all
	poetry build

.PHONY: publish publish-github publish-canvaslms publish-docker
publish: publish-canvaslms doc/canvaslms.pdf publish-docker publish-github

publish-github: doc/canvaslms.pdf
	git push
	gh release create -t v${version} v${version} doc/canvaslms.pdf

doc/canvaslms.pdf: $(wildcard src/canvaslms/cli/*.tex)
	${MAKE} -C $(dir $@) $(notdir $@)

publish-canvaslms: compile
	poetry publish

publish-docker:
	sleep 60
	${MAKE} -C docker publish


.PHONY: clean
clean: clean-makefiles
	${RM} -r __pycache__

# The makefiles submodule is bundled into the sdist (see pyproject.toml), but it
# is not part of SUBDIR, so a top-level clean never descends into it. Its
# PythonTeX runs leave dangling makefiles.pytxcode / pythontex-files-makefiles
# symlinks (pointing into the removed ltxobj dir) that break poetry build. Remove
# them here so clean keeps the tree buildable.
.PHONY: clean-makefiles
clean-makefiles:
	${RM} makefiles/makefiles.pytxcode
	${RM} -R makefiles/pythontex-files-makefiles

.PHONY: distclean
distclean:
	${RM} -R build dist canvaslms.egg-info src/canvaslms.egg-info


INCLUDE_MAKEFILES=makefiles
include ${INCLUDE_MAKEFILES}/subdir.mk
