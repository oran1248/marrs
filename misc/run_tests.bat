
cd ..

rm -rf dist
rm -rf build
rm -rf src/marrs.egg-info

python src/jslib/bundle.py

python setup.py install

python -m pytest -x
