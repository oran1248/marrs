JAVA_CLASS_TO_SIMPLE_CLASS_MAPPING = {
	'int': 'int',
	"java.lang.Integer": "java.lang.Integer",
	"[B": "byte[]",
	"[[I": "int[][]",
	"[[[S": "short[][][]",
	"[J": "long[]",
	"[Z": "boolean[]",
	"[F": "float[]",
	"[[[[D": "double[][][][]",
	"[C": "char[]",
	"[Ljava.lang.Character;": "java.lang.Character[]",
	"[[Ljava.lang.String;": "java.lang.String[][]",
	"[[[Ljava.lang.String;": "java.lang.String[][][]",
}


def test_simplify_java_class_name(simplify_java_class_name_func):
	for java, simple in JAVA_CLASS_TO_SIMPLE_CLASS_MAPPING.items():
		assert simplify_java_class_name_func(java) == simple


def test_simple_class_name_to_java_class_name(simple_class_name_to_java_class_name_func):
	for java, simple in JAVA_CLASS_TO_SIMPLE_CLASS_MAPPING.items():
		assert simple_class_name_to_java_class_name_func(simple) == java
