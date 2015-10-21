build:
	python setup.py build

install:
	python setup.py install

clean:
	rm -rf build dist bravado_bitjws.egg-info tests/__pycache__ bravado_bitjws/__pycache__
	rm -rf tests/*.pyc bravado_bitjws/*.pyc *.egg *~ bravado_bitjws/*~

rst:
	pandoc --from=markdown_github --to=rst --output=README.rst README.md

