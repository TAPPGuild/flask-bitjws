build:
	python setup.py build

install:
	python setup.py install

clean:
	rm -rf build dist bravado_bitjws.egg-info test/__pycache__ bravado_bitjws/__pycache__
	rm -rf test/*.pyc bravado_bitjws/*.pyc *.egg *~ bravado_bitjws/*~ test/*~

rst:
	pandoc --from=markdown_github --to=rst --output=README.rst README.md

