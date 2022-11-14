SUBDIR_GOALS=	all clean distclean

SUBDIR+=		src/canvaslms
SUBDIR+=		doc
SUBDIR+=		docker

version=$(shell sed -n 's/^ *version *= *\"\([^\"]\+\)\",/\1/p' pyproject.toml)


.PHONY: all
all: compile doc/canvaslms.pdf

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

.PHONY: publish publish-canvaslms publish-docker
publish: publish-canvaslms doc/canvaslms.pdf publish-docker
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
clean:

.PHONY: distclean
distclean:
	${RM} -R build dist canvaslms.egg-info src/canvaslms.egg-info


INCLUDE_MAKEFILES=makefiles
include ${INCLUDE_MAKEFILES}/subdir.mk
