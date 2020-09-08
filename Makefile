.PHONY: setup
setup: setup.py
	python3 setup.py bdist_wheel

.PHONY: test-install
test-install:
	pip install -e .

requirements.txt:
	pip freeze > $@

.PHONY: sdist
sdist:
	python setup.py sdist

MANIFEST.in:
	check-manifest --create

.PHONY: publish
publish:
	twine upload dist/*

