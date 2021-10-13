NOWEAVEFLAGS.tex=	-n -delay -t2
NOTANGLEFLAGS.py=


.PHONY: all
all: __init__.py
all: canvasapi.py canvasapi.tex


.PHONY: clean
clean:
	${RM} canvasapi.py canvasapi.tex


INCLUDE_MAKEFILES=../../../makefiles
include ${INCLUDE_MAKEFILES}/tex.mk
include ${INCLUDE_MAKEFILES}/noweb.mk

