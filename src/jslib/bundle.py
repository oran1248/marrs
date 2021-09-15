import glob
import os
import pathlib
import re


def get_dir_path(file_path):
	return pathlib.Path(file_path).parent.resolve()


def main():
	output_filepath = os.path.join(get_dir_path(__file__), '..', 'marrs', 'data', 'bundle.js')
	print('output_filepath', output_filepath)
	lib_dirpath = os.path.join(get_dir_path(__file__), 'lib/*.js')
	print('lib_dirpath', lib_dirpath)
	print(output_filepath)
	with open(output_filepath, 'w') as outfile:
		for filename in glob.glob(lib_dirpath):
			print(filename)
			with open(filename, 'r') as readfile:
				content = readfile.read()
				content = re.sub(r'import .*?;', '', content, flags=re.DOTALL)
				content = re.sub(r'^export ', '', content)
				content = re.sub(r'\nexport ', '', content)
				outfile.write(content + '\n')


if __name__ == "__main__":
	main()
