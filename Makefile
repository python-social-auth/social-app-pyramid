build:
	@ python -m build

publish:
	@ twine upload dist/*

clean:
	@ find . -name '*.py[co]' -delete
	@ find . -name '__pycache__' -delete
	@ rm -rf *.egg-info dist build
