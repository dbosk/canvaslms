# Makefile for canvaslms test suite
#
# Tests are written in .nw files throughout the src/ tree using
# chunks named "<<test modulename.py>>". This Makefile automatically
# discovers those chunks and tangles them to tests/unit/test_*.py files.

# Auto-discover test chunks in .nw files
# Output format: "unit/test_modulename.py:sourcefile.nw:chunk_with_underscores"
# We convert spaces to underscores in the chunk name to avoid word-splitting issues
define find_tests
( \
	find ../src -name '*.nw' | xargs grep -l "<<test [^>]*\.py>>" | \
		while read file; do \
			chunk=$$(grep -o "<<test [^>]*\.py>>" "$$file" | head -1 | \
			         sed 's/<<test \(.*\)\.py>>/\1/'); \
			chunk_safe=$$(echo "$$chunk" | sed 's/ /_/g'); \
			echo "unit/test_$${chunk_safe}.py:$$file:test_$${chunk_safe}.py"; \
		done; \
	[ -f conftest.nw ] && echo "conftest.py:conftest.nw:conftest.py"; \
) | sort -u
endef

# Generate build target for each discovered test
# Input: test_file:source_file:chunk_name_with_underscores
# Convert underscores back to spaces for the actual chunk name
define def_target
$(shell echo $1 | cut -d: -f1): $(shell echo $1 | cut -d: -f2)
	@mkdir -p $$(dir $$@)
	notangle -R"$(shell echo $1 | cut -d: -f3 | sed 's/_/ /g')" $$< | cpif $$@ && noroots $$<
endef

# Discover all tests
TESTS := $(shell $(find_tests))

# Extract just the test filenames for dependencies
TEST_MODULES := $(foreach entry,$(TESTS),$(shell echo $(entry) | cut -d: -f1))

# Also generate .tex for documentation
DOC_MODULES := conftest.tex

# Main targets
.PHONY: all
all: $(TEST_MODULES) $(DOC_MODULES)

# Generate rules for each test
$(foreach entry,$(TESTS),$(eval $(call def_target,$(entry))))

# Documentation generation for conftest
conftest.tex: conftest.nw
	noweave -x -n -delay -t2 $< > $@

# Target to run tests after tangling
.PHONY: test
test: all compile
	poetry run pytest -v --cov=canvaslms --cov-report=term-missing

.PHONY: compile
compile:
	$(MAKE) -C ../src/canvaslms all

# Clean generated test files
.PHONY: clean
clean:
	$(RM) $(TEST_MODULES) $(DOC_MODULES)
	$(RM) -r .pytest_cache __pycache__ unit/__pycache__
	$(RM) -r htmlcov .coverage

INCLUDE_MAKEFILES=../makefiles
include $(INCLUDE_MAKEFILES)/tex.mk
