NOTANGLEFLAGS.py=


.PHONY: all
all: __init__.py
all: canvasapi.py canvasapi.tex
all: attachment_cache.py attachment_cache.tex

.PHONY: clean
clean:
	${RM} canvasapi.py canvasapi.tex
	${RM} attachment_cache.py attachment_cache.tex


INCLUDE_MAKEFILES=../../../makefiles
include ${INCLUDE_MAKEFILES}/tex.mk
include ${INCLUDE_MAKEFILES}/noweb.mk

