def test(test_instance):
	assert len(test_instance.get_fields()) > 1
	assert len(test_instance.get_fields("F")) == 1
	assert test_instance.get("s") == 5
	assert test_instance.call("uu", [7]) == 11
	assert test_instance.to_string() == "ToString1"
