from conftest import TEST_APP_TEST_CLASS_NAME


def test_hooks_static_func(test_agent):
	def my_hook(params, original_retval):
		assert original_retval is None
		assert params[0] == 'aaa'
		return 3

	def call():
		return test_agent.call_static_method(TEST_APP_TEST_CLASS_NAME, "overload", ["aaa"], ['java.lang.String'])

	# Before the hook - returns 1
	assert call() == 1

	# add hook to return 3
	hook = test_agent.hooks.add(TEST_APP_TEST_CLASS_NAME, "overload", ['java.lang.String'], hook_impl=my_hook,
	                            get_original_retval=False)

	# check that 3 is returned
	assert call() == 3

	# disable the hook
	hook.disable()

	# hook is disabled, should return 1 again
	assert call() == 1

	# enable the hook
	hook.enable()

	# enable the hook and check returned value
	assert call() == 3


def test_hooks_return_orig_retval(test_agent):
	def my_hook(params, orig_reval):
		return orig_reval + 1

	def call():
		return test_agent.call_static_method(TEST_APP_TEST_CLASS_NAME, "overload", ["aaa"], ['java.lang.String'])

	test_agent.hooks.add(TEST_APP_TEST_CLASS_NAME, "overload", ['java.lang.String'], hook_impl=my_hook,
	                     get_original_retval=True)

	assert call() == 2
