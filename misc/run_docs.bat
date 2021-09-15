
:: sphinx-apidoc -o source ../src/marrs ^
:: ../src/marrs/consts.py ^
:: ../src/marrs/android_manifest.py ^
:: ../src/marrs/log.py ^
:: ../src/marrs/main.py ^
:: ../src/marrs/storage.py ^
:: ../src/marrs/utils.py

cd ..

rm -rf dist
rm -rf build
rm -rf src/marrs.egg-info

python src/jslib/bundle.py

python setup.py install

rm -rf docs-html

cd docs

cp -r build/html/* .

make clean && make html && python -m http.server