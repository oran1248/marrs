from conftest import TEST_APP_VERSION, TEST_APP_MAIN_ACTIVITY, TEST_APP_PACKAGE_NAME


def test_get_version(test_app):
	assert test_app.get_version() == TEST_APP_VERSION


def test_name(test_app):
	assert test_app.name == TEST_APP_PACKAGE_NAME


def test_get_main_activity(test_app):
	assert test_app.get_main_activity() == TEST_APP_MAIN_ACTIVITY


def test_get_local_apk(test_app):
	apk_path = test_app.get_local_apk_path()
	assert apk_path
	

def test_adv(test_app):
	test_app.uninstall()
	test_app.uninstall()
	assert not test_app.is_installed()
	test_app.install()
	assert test_app.is_installed()
	assert not test_app.is_running()
	test_app.force_stop()
	test_app.clear_data()
	test_app.start()
	assert test_app.is_running()
	test_app.force_stop()
	assert not test_app.is_running()
