def test_device_files(device):
	import os
	import tempfile

	fd, local_path = tempfile.mkstemp()
	try:
		with os.fdopen(fd, 'w') as tmp:
			# do stuff with temp file
			tmp.write('stuff')

		assert os.path.exists(local_path)
		remote_path = '/data/local/tmp/tmpfile.txt'
		if device.files.exists(remote_path):
			assert device.files.remove(remote_path)
		assert not device.files.exists(remote_path)
		device.files.push(local_path, remote_path)
		assert device.files.exists(remote_path)
		os.remove(local_path)
		assert not os.path.exists(local_path)
		device.files.pull(remote_path, local_path)
		assert os.path.exists(local_path)
		assert device.files.remove(remote_path)
		assert not device.files.exists(remote_path)

	finally:
		if os.path.exists(local_path):
			os.remove(local_path)
