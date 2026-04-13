NOTANGLEFLAGS.py=

SUBDIR+=	cli
SUBDIR+=	grades
SUBDIR+=	hacks

MODULES+=	__init__.py canvaslms.tex

.PHONY: all
all: ${MODULES}

.INTERMEDIATE: init.py
init.py: canvaslms.nw
	${NOTANGLE.py}

__init__.py: init.py
	${MV} $< $@


.PHONY: clean
clean:
	${RM} ${MODULES}
	${RM} init.py


INCLUDE_MAKEFILES=../../makefiles
include ${INCLUDE_MAKEFILES}/tex.mk
include ${INCLUDE_MAKEFILES}/noweb.mk
include ${INCLUDE_MAKEFILES}/pkg.mk
include ${INCLUDE_MAKEFILES}/subdir.mk
