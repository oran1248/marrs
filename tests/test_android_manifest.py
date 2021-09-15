from conftest import TEST_APP_PACKAGE_NAME, TEST_APP_VERSION, TEST_APP_MAIN_ACTIVITY


def test_get_package_name(test_app_manifest):
	assert test_app_manifest.get_package_name() == TEST_APP_PACKAGE_NAME


def test_get_package_version(test_app_manifest):
	assert test_app_manifest.get_package_version() == TEST_APP_VERSION


def test_get_main_activity(test_app_manifest):
	assert test_app_manifest.get_main_activity() == TEST_APP_MAIN_ACTIVITY
