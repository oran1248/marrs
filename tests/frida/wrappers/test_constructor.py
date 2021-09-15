def test(test_agent):
	a_class = test_agent.get_loaded_classes(r".*testapp.*\$A")[0]
	ctors = a_class.get_constructors()
	empty_ctor = ctors[0]
	a1 = empty_ctor.new()
	assert a1.get("b") == 1

	int_ctor = ctors[1]
	a2 = int_ctor.new([55])
	assert a2.get("b") == 55
