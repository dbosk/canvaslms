NOTANGLEFLAGS.py=


.PHONY: all
all: __init__.py
all: canvasapi.py canvasapi.tex
all: attachment_cache.py attachment_cache.tex

canvasapi.py: canvasapi.nw
	${NOTANGLE.py}

attachment-cache.py: attachment_cache.nw
	${NOTANGLE.py}

.INTERMEDIATE: attachment-cache.py

attachment_cache.py: attachment-cache.py
	${MV} $< $@


.PHONY: clean
clean:
	${RM} canvasapi.py canvasapi.tex
	${RM} attachment_cache.py attachment_cache.tex


INCLUDE_MAKEFILES=../../../makefiles
include ${INCLUDE_MAKEFILES}/tex.mk
include ${INCLUDE_MAKEFILES}/noweb.mk

