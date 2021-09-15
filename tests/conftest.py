from unittest.mock import MagicMock

import pytest

TEST_APP_APK_RELATIVE_PATH = r"..\test-app\app\build\outputs\apk\debug\app-debug.apk"
TEST_APP_PACKAGE_NAME = "com.example.testapp"
TEST_APP_MAIN_ACTIVITY = "{package}.MainActivity".format(package=TEST_APP_PACKAGE_NAME)
TEST_APP_VERSION = "1.0"

TEST_APP_TEST_CLASS_NAME = "{package}.MyClass".format(package=TEST_APP_PACKAGE_NAME)
TEST_APP_SAMPLE_CLASS = "{package}.SampleClass".format(package=TEST_APP_PACKAGE_NAME)


@pytest.fixture(scope="session")
def test_app_manifest(test_app_apk_path):
	from marrs.android_manifest import AndroidManifest
	return AndroidManifest.from_apk(test_app_apk_path)


@pytest.fixture(scope="session")
def simplify_java_class_name_func():
	from marrs.frida.utils import simplify_java_array_type
	return simplify_java_array_type


@pytest.fixture(scope="session")
def simple_class_name_to_java_class_name_func():
	from marrs.frida.utils import convert_to_api_class_name
	return convert_to_api_class_name


@pytest.fixture(scope="session")
def test_app_apk_path():
	from marrs.log import Log
	Log.set_log_level(Log.DEBUG)
	from marrs.utils import get_dir_path
	from os import path
	apk_path = path.join(get_dir_path(__file__), TEST_APP_APK_RELATIVE_PATH)
	return apk_path


@pytest.fixture(scope="function")
def storage(tmp_path):
	from marrs.storage import Storage
	Storage.set_folder_path(str(tmp_path))
	return Storage


@pytest.fixture(scope="module")
def device():
	from marrs import get_devices
	devices = get_devices(True)
	assert devices
	device = devices[0]
	return device


@pytest.fixture(scope="module")
def test_app(device, test_app_apk_path):
	install = True

	if install:
		test_app = device.install_app(test_app_apk_path, force_install=True)
		assert test_app
		test_app.start()

	test_app = device.get_app(TEST_APP_PACKAGE_NAME)
	assert test_app
	return test_app


@pytest.fixture(scope="module")
def test_agent(test_app):
	test_agent = test_app.attach_frida_agent()
	
	output = test_agent.output
	output.start = MagicMock()
	output.kill = MagicMock()
	output.print = MagicMock()

	assert test_agent
	yield test_agent
	test_agent.kill()


@pytest.fixture(scope="function")
def test_instance(test_agent):
	return test_agent.new_instance(TEST_APP_TEST_CLASS_NAME)
