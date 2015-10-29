build:
	python setup.py build

install:
	python setup.py install

clean:
	rm -rf build dist flask_bitjws.egg-info test/__pycache__
	rm -rf test/*.pyc *.egg *~ *pyc test/*~

rst:
	pandoc --from=markdown_github --to=rst --output=README.rst README.md

