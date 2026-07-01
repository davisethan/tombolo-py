.PHONY: docs
docs:
	pdoc -o docs tombolo

.PHONY: publish
publish:
	rm -rf dist
	python -m build
	twine upload dist/*
