import re

import pytest
from conftest import TEST_APP_TEST_CLASS_NAME, TEST_APP_PACKAGE_NAME, TEST_APP_SAMPLE_CLASS
from marrs.frida.wrappers import Array


def test_run_js(test_agent):
	assert test_agent.run_js("2") == 2
	assert test_agent.run_js("2*4") == 8
	arr = test_agent.run_js("[1,2,3]")
	assert isinstance(arr, Array)
	assert arr.class_name is None
	assert arr.elem_type is None
	assert arr.to_list() == [1, 2, 3]

	integer = test_agent.run_js("JS.newInstance('java.lang.Integer', ['3'])")
	assert integer.class_name == 'java.lang.Integer'
	assert integer.to_string() == "3"
	assert integer.call('intValue') == 3


def test_get_loaded_classes(test_agent):
	classes = test_agent.get_loaded_classes(".*{0}.*".format(TEST_APP_PACKAGE_NAME))
	assert len(classes) == 5


def test_get_methods(test_agent):
	methods = test_agent.get_methods(TEST_APP_TEST_CLASS_NAME, is_static=True)
	assert len(methods) == 10
	methods = test_agent.get_methods(TEST_APP_TEST_CLASS_NAME, is_static=False)
	assert len(methods) == 18
	methods = test_agent.get_methods(TEST_APP_TEST_CLASS_NAME, is_static=None)
	assert len(methods) == 28
	assert len(test_agent.get_methods(TEST_APP_TEST_CLASS_NAME, name_substr="overload")) == 4
	assert len(test_agent.get_methods(TEST_APP_TEST_CLASS_NAME, name_substr="gg")) == 1
	assert len(test_agent.get_methods(TEST_APP_TEST_CLASS_NAME, name_substr="uu")) == 2


def test_get_fields(test_agent):
	fields = test_agent.get_fields(TEST_APP_TEST_CLASS_NAME, is_static=True)
	assert len(fields) == 4
	fields = test_agent.get_fields(TEST_APP_TEST_CLASS_NAME, is_static=False)
	assert len(fields) == 25
	fields = test_agent.get_fields(TEST_APP_TEST_CLASS_NAME, is_static=None)
	assert len(fields) == 29
	assert len(test_agent.get_fields(TEST_APP_TEST_CLASS_NAME, name_substr="sampleClass")) == 2


def test_get_constructors(test_agent):
	ctors = test_agent.get_constructors(TEST_APP_TEST_CLASS_NAME)
	assert len(ctors) == 2
	assert TEST_APP_TEST_CLASS_NAME in str(ctors[0])

	ctors = test_agent.get_constructors(TEST_APP_SAMPLE_CLASS)
	assert len(ctors) == 11


def test_get_instances(test_agent):
	instances = test_agent.get_instances(TEST_APP_TEST_CLASS_NAME)
	assert len(instances) == 1
	instances = test_agent.get_instances(TEST_APP_SAMPLE_CLASS)
	assert len(instances) == 3


def test_create_instance(test_agent):
	instance = test_agent.new_instance("java.lang.String", ["sss"])
	assert instance
	assert instance.class_name == "java.lang.String"
	assert instance.to_string() == 'sss'

	instance = test_agent.new_instance("int", [3])
	assert instance
	assert instance.class_name == "java.lang.Integer"
	assert instance.to_string() == '3'

	instance = test_agent.new_instance("char", ["c"])
	assert instance
	assert instance.class_name == "java.lang.Character"
	assert instance.to_string() == 'c'

	instance = test_agent.new_instance("float", [3.2])
	assert instance
	assert instance.class_name == "java.lang.Float"
	assert instance.to_string() == '3.2'

	instance = test_agent.new_instance("double", [3.2])
	assert instance
	assert instance.class_name == "java.lang.Double"
	assert instance.to_string() == '3.2'

	instance = test_agent.new_instance("boolean", [False])
	assert instance
	assert instance.class_name == "java.lang.Boolean"
	assert instance.to_string() == 'false'

	instance = test_agent.new_instance("java.lang.Integer", [3])
	assert instance
	assert instance.class_name == "java.lang.Integer"
	assert instance.to_string() == '3'

	instance = test_agent.new_instance(TEST_APP_TEST_CLASS_NAME)
	assert instance
	assert instance.class_name == TEST_APP_TEST_CLASS_NAME
	assert instance.to_string() == 'ToString1'

	instance = test_agent.new_instance(TEST_APP_SAMPLE_CLASS)
	assert instance
	assert instance.class_name == TEST_APP_SAMPLE_CLASS
	assert instance.to_string() == 'empty'

	instance = test_agent.new_instance(TEST_APP_SAMPLE_CLASS, [1, 1.1, 'c', "sss", True, 33, 5555, 22.33],
	                                   ['int', 'double', 'char', 'java.lang.String', 'boolean', 'byte', 'long',
	                                    'float'])
	assert instance
	assert instance.class_name == TEST_APP_SAMPLE_CLASS
	assert instance.to_string() == 's1'

	instance = test_agent.new_instance(TEST_APP_SAMPLE_CLASS, [1, 1.1, 'c', "sss", True, 33, 5555, 22.33])
	assert instance
	assert instance.class_name == TEST_APP_SAMPLE_CLASS
	assert instance.to_string() == 's1'

	instance = test_agent.new_instance(TEST_APP_SAMPLE_CLASS,
	                                   [test_agent.new_instance("int", [3]),
	                                    test_agent.new_instance("double", [3.3]),
	                                    test_agent.new_instance("char", ['3']),
	                                    test_agent.new_instance("java.lang.String", ['somestr']),
	                                    test_agent.new_instance("boolean", [True]),
	                                    test_agent.new_instance("byte", [3]),
	                                    test_agent.new_instance("long", [33333]),
	                                    test_agent.new_instance("float", [3.56])])
	assert instance
	assert instance.class_name == TEST_APP_SAMPLE_CLASS
	assert instance.to_string() == 's2'

	instance = test_agent.new_instance(TEST_APP_SAMPLE_CLASS, [3])
	assert test_agent.__get_field_value__(TEST_APP_SAMPLE_CLASS, "s", instance.id) == "i1"

	instance = test_agent.new_instance(TEST_APP_SAMPLE_CLASS, [test_agent.new_instance("int", [3])])
	assert test_agent.__get_field_value__(TEST_APP_SAMPLE_CLASS, "s", instance.id) == "i2"

	instance = test_agent.new_instance(TEST_APP_SAMPLE_CLASS, [test_agent.new_instance("java.lang.Integer", [3])])
	assert test_agent.__get_field_value__(TEST_APP_SAMPLE_CLASS, "s", instance.id) == "i2"

	assert instance
	assert instance.class_name == TEST_APP_SAMPLE_CLASS


def test_get_field_value(test_agent, test_instance):
	def geti(field_name):
		return test_agent.__get_field_value__(TEST_APP_TEST_CLASS_NAME, field_name, test_instance.id)

	def get(field_name):
		return test_agent.get_static_field_value(TEST_APP_TEST_CLASS_NAME, field_name)

	# static fields, primitive instances
	assert get("si") == 100
	assert get("sI").to_string() == "101"
	assert get("sI").class_name == "java.lang.Integer"

	# static fields, class instances
	v = get("sSample")
	assert v.class_name == TEST_APP_SAMPLE_CLASS
	assert v.id

	# static field, null value
	assert get("sSampleNull") is None

	# instance field, primitive instances
	assert geti("b") == 1
	assert geti("B").to_string() == "2"
	assert geti("i") == 3
	assert geti("I").to_string() == "4"
	assert geti("s") == 5
	assert geti("S").to_string() == "6"
	assert geti("d") == 7.7
	assert geti("D").to_string() == "8.8"
	assert "{:.1f}".format(geti("f")) == '7.7'
	assert geti("F").to_string() == "8.8"
	assert geti("c") == "c"
	assert geti("C").to_string() == "C"
	assert geti("bool") is True
	assert geti("Bool").to_string() == 'false'
	assert geti("Str") == "sample-string..."

	# instance field, class instances
	assert geti("someNullValue") is None
	v = geti("sampleClassInstance")
	assert v.class_name == TEST_APP_SAMPLE_CLASS
	assert v.id

	# check that the type that return is the dynamic type
	v = geti("itsb")
	assert v.class_name == TEST_APP_TEST_CLASS_NAME + "$B"

	v = geti("as")
	assert isinstance(v, Array)
	assert v.class_name == 'java.lang.String[]'

	v = geti("ai")
	assert isinstance(v, Array)
	assert v.class_name == 'int[][]'

	v = geti("aI")
	assert isinstance(v, Array)
	assert v.class_name == 'java.lang.Integer[][][]'


def test_set_field_value(test_agent, test_instance):
	def geti(field_name):
		return test_agent.__get_field_value__(TEST_APP_TEST_CLASS_NAME, field_name, test_instance.id)

	def get(field_name):
		return test_agent.get_static_field_value(TEST_APP_TEST_CLASS_NAME, field_name)

	def seti(field_name, new_value):
		return test_agent.__set_field_value__(TEST_APP_TEST_CLASS_NAME, field_name, new_value, test_instance.id)

	def set(field_name, new_value):
		return test_agent.set_static_field_value(TEST_APP_TEST_CLASS_NAME, field_name, new_value)

	# static fields, primitive instances
	set("si", 200)
	assert get("si") == 200

	set("sI", test_agent.new_instance("java.lang.Integer", [3]))
	assert get("sI").to_string() == "3"
	assert get("sI").class_name == "java.lang.Integer"

	# static fields, class instances
	set("sSample", None)
	v = get("sSample")
	assert v is None

	sample = test_agent.new_instance(TEST_APP_SAMPLE_CLASS,
	                                 [test_agent.new_instance("int", [3]),
	                                  test_agent.new_instance("double", [3.3]),
	                                  test_agent.new_instance("char", ['3']),
	                                  test_agent.new_instance("java.lang.String", ['somestr']),
	                                  test_agent.new_instance("boolean", [True]),
	                                  test_agent.new_instance("byte", [3]),
	                                  test_agent.new_instance("long", [33333]),
	                                  test_agent.new_instance("float", [3.56])])
	set("sSample", sample)
	v = get("sSample")
	assert v
	assert v.class_name == TEST_APP_SAMPLE_CLASS
	assert v.to_string() == 's2'

	# static field, null value
	assert get("sSampleNull") is None

	# instance field, primitive instances
	seti("b", 55)
	assert geti("b") == 55

	seti("B", test_agent.new_instance("java.lang.Byte", [3]))
	assert geti("B").to_string() == "3"

	seti("i", 87)
	assert geti("i") == 87

	seti("I", test_agent.new_instance("java.lang.Integer", [3]))
	assert geti("I").to_string() == "3"

	seti("s", 45)
	assert geti("s") == 45

	seti("S", test_agent.new_instance("java.lang.Short", [32]))
	assert geti("S").to_string() == "32"

	seti("d", 9.91)
	assert geti("d") == 9.91

	seti("D", test_agent.new_instance("java.lang.Double", [32.32]))
	assert geti("D").to_string() == "32.32"

	seti("f", 3.3)
	assert "{:.1f}".format(geti("f")) == '3.3'

	seti("F", test_agent.new_instance("java.lang.Float", [12.32]))
	assert geti("F").to_string() == "12.32"

	seti("c", 'w')
	assert geti("c") == "w"

	seti("C", test_agent.new_instance("java.lang.Character", ['T']))
	assert geti("C").to_string() == "T"

	seti("bool", False)
	assert geti("bool") is False

	seti("Bool", test_agent.new_instance("java.lang.Boolean", [True]))
	assert geti("Bool").to_string() == 'true'

	seti("Str", test_agent.new_instance("java.lang.String", ['hello']))
	assert geti("Str") == "hello"

	# instance field, class instances
	instance = test_agent.new_instance(TEST_APP_SAMPLE_CLASS, [1, 1.1, 'c', "sss", True, 33, 5555, 22.33],
	                                   ['int', 'double', 'char', 'java.lang.String', 'boolean', 'byte', 'long',
	                                    'float'])
	seti("someNullValue", instance)
	v = geti("sampleClassInstance")
	assert v.to_string() == 's1'

	# check that the type that return is the dynamic type
	a_instance = test_agent.new_instance(TEST_APP_TEST_CLASS_NAME + "$A")
	seti("itsb", a_instance)
	assert geti("itsb").class_name == TEST_APP_TEST_CLASS_NAME + "$A"
	b_instance = test_agent.new_instance(TEST_APP_TEST_CLASS_NAME + "$B")
	seti("itsb", b_instance)
	assert geti("itsb").class_name == TEST_APP_TEST_CLASS_NAME + "$B"

	seti("as", ['a', 'b', 'c'])
	v = geti("as")
	assert isinstance(v, Array)
	assert v.class_name == 'java.lang.String[]'
	assert str(v) == '[a, b, c]'

	seti("ai", test_agent.new_array('int[][]', [[1], [2, 9], [3]]))
	v = geti("ai")
	assert isinstance(v, Array)
	assert v.class_name == 'int[][]'
	assert str(v) == '[[1], [2, 9], [3]]'

	seti("aI", test_agent.new_array('java.lang.Integer[][][]', [[[1]], [[2], [9]], [[3]]]))
	v = geti("aI")
	assert isinstance(v, Array)
	assert v.class_name == 'java.lang.Integer[][][]'
	assert str(v) == '[[[1]], [[2], [9]], [[3]]]'


def test_to_string(test_agent):
	instance = test_agent.new_instance(TEST_APP_SAMPLE_CLASS, [3])
	assert test_agent.__to_string__(instance.id) == "i1"

	instance = test_agent.new_instance(TEST_APP_SAMPLE_CLASS, [test_agent.new_instance("int", [3])])
	assert test_agent.__to_string__(instance.id) == "i2"


def test_call_static_method(test_agent):
	# call static methods
	assert test_agent.call_static_method(TEST_APP_TEST_CLASS_NAME, "overload", [""], ["java.lang.String"]) == 1
	double_instance = test_agent.new_instance("java.lang.Double", [3.2])
	assert test_agent.call_static_method(TEST_APP_TEST_CLASS_NAME, "overload",
	                                     [1, double_instance],
	                                     ["int", "java.lang.Double"]) is None
	assert test_agent.call_static_method(TEST_APP_TEST_CLASS_NAME, "voidFunc") is None
	assert test_agent.call_static_method(TEST_APP_TEST_CLASS_NAME, "f", [1, 3], ['int', 'double']) == 3
	assert test_agent.call_static_method(TEST_APP_TEST_CLASS_NAME, "f", [2, 3.2], ['int', 'double']) == 6.4
	assert test_agent.call_static_method(TEST_APP_TEST_CLASS_NAME, "f", [2, 2.2], ['int', 'double']) == 4.4

	arr = test_agent.call_static_method(TEST_APP_TEST_CLASS_NAME, "sgetArr", ["hello"], ["java.lang.String"])
	assert isinstance(arr, Array)
	assert arr.class_name is None
	print(str(arr))
	assert re.match(r"\[.*Ainstance.*Binstance.*\]", str(arr))

	arr = test_agent.call_static_method(TEST_APP_TEST_CLASS_NAME, "sgetArr2", ['c'], ["char"])
	assert isinstance(arr, Array)
	assert arr.class_name is None
	assert re.match(r"\[.*Binstance.*Binstance.*Binstance.*Binstance.*\]", str(arr))

	arr = test_agent.call_static_method(TEST_APP_TEST_CLASS_NAME, "sgetArr3", [99], ["short"])
	assert isinstance(arr, Array)
	assert arr.class_name is None
	assert "[[[1, 2]], [[3, 4]]]" == str(arr)


# TODO: call a method that gets an array as param


def test_create_array_1d(test_agent):
	arr = test_agent.new_array("int[]", [1, 2])
	assert arr.class_name == "int[]"
	assert '[1, 2]' == str(arr)
	arr[1] = 3
	arr[0] = 7
	assert '[7, 3]' == str(arr)

	arr = test_agent.new_array("java.lang.Integer[]", [test_agent.new_instance('java.lang.Integer', [1]),
	                                                   test_agent.new_instance('java.lang.Integer', [2]),
	                                                   test_agent.new_instance('java.lang.Integer', [3])])
	assert arr.class_name == "java.lang.Integer[]"
	assert '[1, 2, 3]' == str(arr)
	arr[1] = test_agent.new_instance('java.lang.Integer', [3])
	assert '[1, 3, 3]' == str(arr)

	arr = test_agent.new_array('double[]', [1.1, 2, 3])
	assert arr.class_name == "double[]"
	assert '[1.1, 2, 3]' == str(arr)
	arr[2] = 7.2
	assert '[1.1, 2, 7.2]' == str(arr)

	i1 = test_agent.new_instance(TEST_APP_SAMPLE_CLASS)
	i2 = test_agent.new_instance(TEST_APP_SAMPLE_CLASS, [2])
	i3 = test_agent.new_instance(TEST_APP_SAMPLE_CLASS, ['3'])

	arr = test_agent.new_array(TEST_APP_SAMPLE_CLASS + "[]", [i1, i2, i3])
	assert arr.class_name == TEST_APP_SAMPLE_CLASS + "[]"
	assert "[empty, i1, 3]" == str(arr)


def test_call_instance_method(test_agent, test_instance):
	# call instance methods
	assert test_agent.__call_instance_method__(test_instance.id, "overload", [], []) is None
	assert test_agent.__call_instance_method__(test_instance.id, "gg", [None, None, 1],
	                                           ["java.lang.String", "java.lang.Object", "byte"]
	                                           ) == -1
	assert test_agent.__call_instance_method__(test_instance.id, "gg",
	                                           ["hi", test_agent.new_instance("java.lang.Object"), 1],
	                                           ["java.lang.String", "java.lang.Object", "byte"]) == -1

	sc1 = test_agent.new_instance(TEST_APP_SAMPLE_CLASS)
	sc2 = test_agent.new_instance(TEST_APP_SAMPLE_CLASS)
	assert test_agent.__call_instance_method__(test_instance.id, "sampleString", [sc1, sc2, "2", 3],
	                                           [TEST_APP_SAMPLE_CLASS, TEST_APP_SAMPLE_CLASS, "java.lang.String",
	                                            "int"]) == "emptyempty23"

	assert test_agent.__call_instance_method__(test_instance.id, "uu", [3], ["int"]) == 11
	assert test_agent.__call_instance_method__(test_instance.id, "uu",
	                                           [test_agent.new_instance('java.lang.Integer', [3])],
	                                           ["java.lang.Integer"]) == 22
	assert test_agent.__call_instance_method__(test_instance.id, "uu", [test_agent.new_instance("int", [3])],
	                                           ["java.lang.Integer"]) == 22

	# func return an array
	arr = test_agent.__call_instance_method__(test_instance.id, "getArr", ["mys"], ["java.lang.String"])
	assert isinstance(arr, Array)
	assert arr.length() == 3
	assert len(arr) == 3
	assert "[1, 2, 3]" == str(arr)
	for i in range(3):
		assert i + 1 == arr[i]

	arr = test_agent.__call_instance_method__(test_instance.id, "getArr2", ['3'], ["char"])
	assert isinstance(arr, Array)
	assert "[[1], [2, 3], [3]]" == str(arr)

	arr = test_agent.__call_instance_method__(test_instance.id, "getArr3", [4], ["short"])
	assert isinstance(arr, Array)
	assert "[[[1, 2]], [[3, 4]]]" == str(arr)

	# func get an array as param
	assert test_agent.__call_instance_method__(test_instance.id, "a1", [[3, 2, 1]], ["int[]"]) == 3

	arr = test_agent.new_array("int[][]", [[18, 2, 3], [12, 1, 1], [2, 2, 2]])
	assert test_agent.__call_instance_method__(test_instance.id, "a2", [arr], ["int[][]"]) == 12
	assert test_agent.__call_instance_method__(test_instance.id, "a2", [[[18, 2, 3], [12, 1, 1], [2, 2, 2]]],
	                                           ["int[][]"]) == 12
	assert test_agent.__call_instance_method__(test_instance.id, "a3", [[[[1, 1], [2, 2]], [[3, 3], [4, 4]]]],
	                                           ["int[][][]"]) == 4
	assert test_agent.__call_instance_method__(test_instance.id, "arrayFunc", [[1, 2, 3], 1.5],
	                                           ["int[]", "double"]) == 9
	assert test_agent.__call_instance_method__(test_instance.id, "arrayFunc",
	                                           [[test_agent.new_instance('java.lang.Integer', [1]),
	                                             test_agent.new_instance('java.lang.Integer', [2]),
	                                             test_agent.new_instance('java.lang.Integer', [3])],
	                                            test_agent.new_instance('java.lang.Double', [1.5])],
	                                           ["java.lang.Integer[]", "java.lang.Double"]) == 2

	assert test_agent.__call_instance_method__(test_instance.id, "darrayFunc", [[["a", "b"], ["c"], ["d", "e", "f"]]],
	                                           ["java.lang.String[][]"]) == 'abcdef'


def test_create_array_2d(test_agent):
	row1 = test_agent.new_array("int[]", [1, 2])
	row2 = test_agent.new_array("int[]", [3, 4])
	arr = test_agent.new_array("int[][]", [row1, row2, [5, 6]])
	assert arr.class_name == "int[][]"
	assert '[[1, 2], [3, 4], [5, 6]]' == str(arr)
	row2[1] = 8
	assert '[[1, 2], [3, 8], [5, 6]]' == str(arr)
	arr[0][1] = 8
	assert '[[1, 8], [3, 8], [5, 6]]' == str(arr)

	arr = test_agent.new_array('int[][]', [[1, 2], [3, 4]])
	assert isinstance(arr, Array)
	assert arr.class_name == "int[][]"
	assert "[[1, 2], [3, 4]]" == str(arr)

	arr = test_agent.new_array("float[][]", [[], []])
	arr[0] = [3, 2]
	assert '[[3, 2], []]' == str(arr)
	arr[1] = [9, 2, 3]
	assert '[[3, 2], [9, 2, 3]]' == str(arr)
	arr[0] = [-1, 0, 888]
	assert '[[-1, 0, 888], [9, 2, 3]]' == str(arr)


def test_create_array_complex(test_agent):
	size = 3
	arr = test_agent.new_array("double[][][]", [[[0], [0], [0]], [[0], [0], [0]], [[0], [0], [0]]])
	assert arr.class_name == "double[][][]"
	for i in range(size):
		for j in range(size):
			arr[i][j][0] = 1

	s = 0
	for i in range(size):
		for j in range(size):
			s += arr[i][j][0]

	assert s == 9

	size = 2
	arr = test_agent.new_array('java.lang.String[][][]', [[[]], [[]]])
	assert arr.class_name == "java.lang.String[][][]"
	assert '[[[]], [[]]]' == str(arr)
	for i in range(len(arr)):
		arr[i] = [['a', 'a']] * size

	assert len(arr) == 2
	assert len(arr[0]) == 2
	assert len(arr[0][0]) == 2

	s = ''
	for i in range(len(arr)):
		for j in range(len(arr[i])):
			for k in range(len(arr[i][j])):
				s += arr[i][j][k]

	assert s == 'a' * size * size * size


def test_create_instance_different_ctors(test_agent):
	instance = test_agent.new_instance(TEST_APP_SAMPLE_CLASS)
	assert test_agent.__get_field_value__(TEST_APP_SAMPLE_CLASS, "s", instance.id) == "empty"

	instance = test_agent.new_instance(TEST_APP_SAMPLE_CLASS, [3])
	assert test_agent.__get_field_value__(TEST_APP_SAMPLE_CLASS, "s", instance.id) == "i1"

	instance = test_agent.new_instance(TEST_APP_SAMPLE_CLASS, [3])
	assert test_agent.__get_field_value__(TEST_APP_SAMPLE_CLASS, "s", instance.id) == "i1"

	instance = test_agent.new_instance(TEST_APP_SAMPLE_CLASS, [test_agent.new_instance('java.lang.Integer', [3])])
	assert test_agent.__get_field_value__(TEST_APP_SAMPLE_CLASS, "s", instance.id) == "i2"

	instance = test_agent.new_instance(TEST_APP_SAMPLE_CLASS, [test_agent.new_instance('java.lang.Integer', [3])])
	assert test_agent.__get_field_value__(TEST_APP_SAMPLE_CLASS, "s", instance.id) == "i2"

	instance = test_agent.new_instance(TEST_APP_SAMPLE_CLASS, ["3"], ['java.lang.String'])
	assert test_agent.__get_field_value__(TEST_APP_SAMPLE_CLASS, "s", instance.id) == "3"

	instance = test_agent.new_instance(TEST_APP_SAMPLE_CLASS,
	                                   [1, 1, '1', test_agent.new_instance('java.lang.String', ["3"]), False, 1, 1,
	                                    9.1],
	                                   ['int', 'double', 'char', 'java.lang.String', 'boolean', 'byte', 'long',
	                                    'float'])
	assert test_agent.__get_field_value__(TEST_APP_SAMPLE_CLASS, "s", instance.id) == "s1"

	instance = test_agent.new_instance(TEST_APP_SAMPLE_CLASS, [1, 1, '1', '1', False, 1, 1, 1],
	                                   ['java.lang.Integer', 'java.lang.Double', 'java.lang.Character',
	                                    'java.lang.String', 'java.lang.Boolean', 'java.lang.Byte', 'java.lang.Long',
	                                    'java.lang.Float'])
	assert test_agent.__get_field_value__(TEST_APP_SAMPLE_CLASS, "s", instance.id) == "s2"

	arr = test_agent.new_array('int[]', [2, 3])
	instance = test_agent.new_instance(TEST_APP_SAMPLE_CLASS, [arr], ['int[]'])
	assert test_agent.__get_field_value__(TEST_APP_SAMPLE_CLASS, "sum", instance.id) == 5

	instance = test_agent.new_instance(TEST_APP_SAMPLE_CLASS, [[1, 2]], ['int[]'])
	assert test_agent.__get_field_value__(TEST_APP_SAMPLE_CLASS, "sum", instance.id) == 3

	arr = test_agent.new_array('int[][]', [[1, 2], [3, 3]])
	instance = test_agent.new_instance(TEST_APP_SAMPLE_CLASS, [arr], ['int[][]'])
	assert test_agent.__get_field_value__(TEST_APP_SAMPLE_CLASS, "sum", instance.id) == 9

	instance = test_agent.new_instance(TEST_APP_SAMPLE_CLASS, [[[1, 2], [3, 2]]], ['int[][]'])
	assert test_agent.__get_field_value__(TEST_APP_SAMPLE_CLASS, "sum", instance.id) == 8

	row1 = test_agent.new_array("int[]", [1, 2])
	row2 = test_agent.new_array("int[]", [3, 4])
	arr = test_agent.new_array("int[][]", [row1, row2, [5, 6]])

	instance = test_agent.new_instance(TEST_APP_SAMPLE_CLASS, [arr], ['int[][]'])
	assert test_agent.__get_field_value__(TEST_APP_SAMPLE_CLASS, "sum", instance.id) == 21


def test_create_instance_exception(test_agent):
	for s in ["int[]", "java.lang.Integer[][]"]:
		with pytest.raises(ValueError, match=r".*array.*"):
			test_agent.new_instance(s)
