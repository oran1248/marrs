def test(test_agent):
	a_class = test_agent.get_loaded_classes(r".*testapp.*\$A")[0]
	print(a_class)
	assert len(a_class.get_methods()) == 4
	assert len(a_class.get_fields()) == 2
	assert len(a_class.get_constructors()) == 2
	num_instances = len(a_class.get_instances())
	assert a_class.get_field("a") == 9
	a_class.set_field("a", 2)
	assert a_class.get_field("a") == 2
	new_instance = a_class.new([2])
	assert num_instances + 1 == len(a_class.get_instances())
