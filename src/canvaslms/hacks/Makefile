NOTANGLEFLAGS.py=


.PHONY: all
all: __init__.py
all: canvasapi_patch.py canvasapi_patch.tex


.PHONY: clean
clean:
	${RM} canvasapi_patch.py canvasapi_patch.tex


INCLUDE_MAKEFILES=../../../makefiles
include ${INCLUDE_MAKEFILES}/tex.mk
include ${INCLUDE_MAKEFILES}/noweb.mk

