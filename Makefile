SUBDIR_GOALS=	all clean distclean

SUBDIR+=		doc
SUBDIR+=		src/canvaslms

version=$(shell sed -n 's/^ *version *= *\"\([^\"]\+\)\",/\1/p' setup.py)
dist=$(addprefix dist/canvaslms-${version}, -py3-none-any.whl .tar.gz)


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

.PHONY: publish publish-canvaslms publish-docker
publish: publish-canvaslms doc/canvaslms.pdf
	git push
	gh release create -t v${version} v${version} doc/canvaslms.pdf

doc/canvaslms.pdf: $(wildcard src/canvaslms/cli/*.tex)
	${MAKE} -C $(dir $@) $(notdir $@)

publish-canvaslms: ${dist}
	python3 -m twine upload -r pypi ${dist}

${dist}: compile canvaslms.bash
	python3 setup.py sdist bdist_wheel

canvaslms.bash:
	register-python-argcomplete canvaslms > $@

#publish-docker:
#	sleep 60
#	${MAKE} -C docker publish


.PHONY: clean
clean:
	${RM} canvaslms.bash

.PHONY: distclean
distclean:
	${RM} -R build dist canvaslms.egg-info src/canvaslms.egg-info


INCLUDE_MAKEFILES=makefiles
include ${INCLUDE_MAKEFILES}/subdir.mk
