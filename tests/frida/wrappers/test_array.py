import pytest


def test(test_agent):
	arr = test_agent.new_array("int[]", [1, 2, 3])

	assert str(arr) == '[1, 2, 3]'
	assert len(arr) == 3

	with pytest.raises(IndexError):
		arr[-1]

	with pytest.raises(IndexError):
		arr[3]

	arr[1] = 3
	assert arr[1] == 3
	assert str(arr) == '[1, 3, 3]'
	assert len(arr.to_list()) == 3
