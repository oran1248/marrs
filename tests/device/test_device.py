from conftest import TEST_APP_PACKAGE_NAME, TEST_APP_VERSION


def test_get_arch(device):
	assert device.get_arch()


def test_get_android_version(device):
	assert device.get_android_version()


def test_get_api_level(device):
	assert device.get_api_level()


def test_is_rooted(device):
	assert device.is_rooted() is True


def test_get_apps_substr_no_results(device):
	apps = device.get_apps("very-bad-pattern")
	assert apps == []


def test_get_apps_empty_substr_get_all_apps(device):
	assert len(device.get_apps("")) == len(device.get_apps())


def test_get_app_version(device, test_app):
	assert device.get_app_version(TEST_APP_PACKAGE_NAME) == TEST_APP_VERSION


def test_test_app_funcs(device, test_app_apk_path):
	# Check uninstall twice
	device.uninstall_app(TEST_APP_PACKAGE_NAME)
	device.uninstall_app(TEST_APP_PACKAGE_NAME)
	assert not device.is_app_installed(TEST_APP_PACKAGE_NAME)
	device.install_app(test_app_apk_path)
	assert device.is_app_installed(TEST_APP_PACKAGE_NAME)
	assert device.get_app_version(TEST_APP_PACKAGE_NAME) == TEST_APP_VERSION
	assert not device.is_app_running(TEST_APP_PACKAGE_NAME)
	device.start_app(TEST_APP_PACKAGE_NAME)
	assert device.is_app_running(TEST_APP_PACKAGE_NAME)
	device.force_stop_app(TEST_APP_PACKAGE_NAME)
	device.clear_app_data(TEST_APP_PACKAGE_NAME)
	assert not device.is_app_running(TEST_APP_PACKAGE_NAME)


def test_frida_funcs(device, storage):
	# Will download frida server from the internet
	device.run_frida_server()
	assert device.is_frida_server_running()
	device.kill_frida_server()
	assert not device.is_frida_server_running()

	# Will use the frida server bin that's already exists on the device
	device.run_frida_server()
	assert device.is_frida_server_running()
	device.kill_frida_server()
	assert not device.is_frida_server_running()

	# Will take frida server from the storage
	device.delete_frida_server()
	device.run_frida_server()
	assert device.is_frida_server_running()
	device.kill_frida_server()
	assert not device.is_frida_server_running()
