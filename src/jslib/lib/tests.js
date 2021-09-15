const assert = (realVal, expectedVal) => {
    if (assert.num === undefined) {
        assert.num = 1;
    } else {
        assert.num++;
    }

    if (realVal !== expectedVal) {
        const s = "assert #" + assert.num + " failed: real='" + realVal + "' ('" + typeof (realVal) + "'), expected='" + expectedVal + "' ('" + typeof (expectedVal) + "')"
        console.log(s);
        throw new Error(s);
    }
}

const roundNum = (num, decimalDigits = 2) => {
    return Number(num.toFixed(decimalDigits))
}

export const runTests = () => {
    const TEST_CLASS = "com.example.testapp.MyClass";
    const SAMPLE_CLASS = "com.example.testapp.SampleClass";

    const INTEGER_CLASS = 'java.lang.Integer';
    const DOUBLE_CLASS = 'java.lang.Double';
    const FLOAT_CLASS = 'java.lang.Float';
    const CHARACTER_CLASS = 'java.lang.Character';
    const BOOLEAN_CLASS = 'java.lang.Boolean';
    const STRING_CLASS = 'java.lang.String';
    const BYTE_CLASS = 'java.lang.Byte';
    const LONG_CLASS = 'java.lang.Long';

    console.log("============================================== JS.newInstance / JS.newArray =========================================================")

    // wrappers
    console.log("wrappers")
    const I1 = JS.newInstance(INTEGER_CLASS, [1]);
    assert(JS.getClassName(I1), INTEGER_CLASS)
    assert(I1.toString(), "1");

    const I2 = JS.newInstance(INTEGER_CLASS, [I1.toString()]);
    assert(JS.getClassName(I2), INTEGER_CLASS)
    assert(I2.toString(), "1");

    const I3 = JS.newInstance(INTEGER_CLASS, [I2.toString()], [STRING_CLASS]);
    assert(JS.getClassName(I3), INTEGER_CLASS)
    assert(I3.toString(), "1");

    const D1 = JS.newInstance(DOUBLE_CLASS, [1.34]);
    assert(JS.getClassName(D1), DOUBLE_CLASS)
    assert(D1.toString(), "1.34");

    const L1 = JS.newInstance(LONG_CLASS, [1123]);
    assert(JS.getClassName(L1), LONG_CLASS)
    assert(L1.toString(), "1123");

    const F1 = JS.newInstance(FLOAT_CLASS, [1.12]);
    assert(JS.getClassName(F1), FLOAT_CLASS)
    assert(F1.toString(), "1.12");

    const C1 = JS.newInstance(CHARACTER_CLASS, ['c']);
    assert(JS.getClassName(C1), CHARACTER_CLASS)
    assert(C1.toString(), "c");

    const B1 = JS.newInstance(BOOLEAN_CLASS, [false]);
    assert(JS.getClassName(B1), BOOLEAN_CLASS)
    assert(B1.toString(), "false");

    const BY1 = JS.newInstance(BYTE_CLASS, [7]);
    assert(JS.getClassName(BY1), BYTE_CLASS)
    assert(BY1.toString(), "7");


    // arrays
    console.log("arrays")
    const integerArr2D = JS.newArray('[L' + INTEGER_CLASS + ';', [[I1], [I2], [I3]]);
    const intArr = JS.newArray('I', [1, 2, 3]);
    const intArr2D = JS.newArray('[I', [[1], [2], [3]]);
    const integerArr = JS.newArray('L' + INTEGER_CLASS + ';', [I1, I2, I3, I3]);

    // classes
    console.log("classes")
    const STRING1 = JS.newInstance(STRING_CLASS, ["STRING1"]);
    assert(JS.getClassName(STRING1), STRING_CLASS)
    assert(STRING1.toString(), "STRING1");

    const STRING2 = JS.newInstance(STRING_CLASS, [STRING1]);
    assert(JS.getClassName(STRING2), STRING_CLASS)
    assert(STRING2.toString(), "STRING1");

    const STRING3 = JS.newInstance(STRING_CLASS, [STRING2], [STRING_CLASS]);
    assert(JS.getClassName(STRING3), STRING_CLASS)
    assert(STRING3.toString(), "STRING1");

    const test1 = JS.newInstance(TEST_CLASS);
    assert(JS.getClassName(test1), TEST_CLASS)
    assert(test1.tmp.value, -7)

    const test2 = JS.newInstance(TEST_CLASS, [test1]);
    assert(JS.getClassName(test2), TEST_CLASS)
    assert(test2.tmp.value, 120)

    const test3 = JS.newInstance(TEST_CLASS, [test2], [TEST_CLASS]);
    assert(JS.getClassName(test3), TEST_CLASS)
    assert(test3.tmp.value, 120)

    const sample0 = JS.newInstance(SAMPLE_CLASS)
    assert(JS.getClassName(sample0), SAMPLE_CLASS)
    assert(sample0.sum.value, -1)

    const sample1 = JS.newInstance(SAMPLE_CLASS, [1], ['int'])
    assert(sample1.s.value, 'i1')

    const sample2 = JS.newInstance(SAMPLE_CLASS, [I3]);
    assert(sample2.s.value, 'i2')

    const sample3 = JS.newInstance(SAMPLE_CLASS, [integerArr2D], ['[[L' + INTEGER_CLASS + ';'])
    assert(sample3.sum.value, -3)

    const sample4 = JS.newInstance(SAMPLE_CLASS, [[[-1, -2, -3], [0, 1, 2, 3, 80], [], []]])
    assert(sample4.sum.value, 80)

    const sample5 = JS.newInstance(SAMPLE_CLASS, [[[I1, I2, I3], [], [], []]], ['[[L' + INTEGER_CLASS + ';'])
    assert(sample5.sum.value, -3)

    const sample6 = JS.newInstance(SAMPLE_CLASS, [intArr], ['[I']);
    assert(sample6.sum.value, 6)

    const sample7 = JS.newInstance(SAMPLE_CLASS, [integerArr], ['[L' + INTEGER_CLASS + ';']);
    assert(sample7.sum.value, -4)

    const sample8 = JS.newInstance(SAMPLE_CLASS, [intArr2D], ['[[I']);
    assert(sample8.sum.value, 6)

    const sample9 = JS.newInstance(SAMPLE_CLASS,
        [I1, D1, C1, STRING1, B1, BY1, L1, F1],
        [INTEGER_CLASS, DOUBLE_CLASS, CHARACTER_CLASS, STRING_CLASS, BOOLEAN_CLASS, BYTE_CLASS, LONG_CLASS, FLOAT_CLASS]
    );
    assert(sample9.s.value, "s2")

    const sample10 = JS.newInstance(SAMPLE_CLASS,
        [1, 2, 'c', 's', false, 11, 22, 33],
        ['int', 'double', 'char', STRING_CLASS, 'boolean', 'byte', 'long', 'float']
    );
    assert(sample10.s.value, "s1")

    const sample11 = JS.newInstance(SAMPLE_CLASS,
        [I1, D1, C1, STRING1, B1, BY1, L1, F1]
    );
    assert(sample11.s.value, "s2")

    const sample12 = JS.newInstance(SAMPLE_CLASS,
        [1, 2, 'c', 's', false, 11, 22, 33]
    );
    assert(sample12.s.value, "s1")


    console.log("============================================== JS.getInstanceFieldValue =========================================================")
    assert(JS.getInstanceFieldValue(test1, "b"), 1) // primitive type
    assert(JS.getInstanceFieldValue(test1, "i"), 3) // primitive type
    assert(roundNum(JS.getInstanceFieldValue(test1, "f")), 7.7) // primitive type
    assert(JS.getInstanceFieldValue(test1, "bool"), true) // primitive type
    assert(JS.getInstanceFieldValue(test1, "B").intValue(), 2) // class type
    assert(JS.getInstanceFieldValue(test1, "sampleClassInstance").s.value, 's1') // class type
    assert(JS.getClassName(JS.getInstanceFieldValue(test1, "sampleClassInstance")), SAMPLE_CLASS)
    assert(JS.getInstanceFieldValue(test1, "someNullValue"), null) // class type - null value
    assert(JS.getClassName(JS.getInstanceFieldValue(test1, "someNullValue")), undefined)
    const stringArr = JS.getInstanceFieldValue(test1, "as"); // arr type
    assert(stringArr.isArray, true);
    assert(stringArr.elemType, 'L' + STRING_CLASS + ';');
    assert(JS.getClassName(stringArr), '[L' + STRING_CLASS + ';');

    const intArr2 = JS.getInstanceFieldValue(test1, "ai");
    assert(intArr2.isArray, true);
    assert(intArr2.elemType, '[I');
    assert(JS.getClassName(intArr2), '[[I');

    const intArr3 = JS.getInstanceFieldValue(test1, "aii");
    assert(intArr3.isArray, true);
    assert(intArr3.elemType, 'I');
    assert(JS.getClassName(intArr3), '[I');

    const integerArr4 = JS.getInstanceFieldValue(test1, "aI");
    assert(integerArr4.isArray, true);
    assert(integerArr4.elemType, '[[L' + INTEGER_CLASS + ";");
    assert(JS.getClassName(integerArr4), '[[[L' + INTEGER_CLASS + ";");

    console.log("============================================== JS.getStaticFieldValue =========================================================")
    assert(JS.getStaticFieldValue(TEST_CLASS, "si"), 100) // primitive type
    assert(JS.getStaticFieldValue(TEST_CLASS, "sI").intValue(), 101) // class type
    assert(JS.getStaticFieldValue(TEST_CLASS, "sSample").toString(), "ToString2") // class type
    assert(JS.getStaticFieldValue(TEST_CLASS, "sSampleNull"), null) // class type

    console.log("============================================== JS.setInstanceFieldValue =========================================================")
    JS.setInstanceFieldValue(test1, "b", 2); // primitive type
    assert(JS.getInstanceFieldValue(test1, "b"), 2)

    JS.setInstanceFieldValue(sample1, "sum", 12) // primitive type
    assert(JS.getInstanceFieldValue(sample1, "sum"), 12)

    JS.setInstanceFieldValue(test1, "bool", false); // primitive type
    assert(JS.getInstanceFieldValue(test1, "bool"), false)

    JS.setInstanceFieldValue(test1, "B", null); // class type
    assert(JS.getInstanceFieldValue(test1, "B"), null)

    JS.setInstanceFieldValue(test1, "B", JS.newInstance(BYTE_CLASS, [10])); // class type
    assert(JS.getInstanceFieldValue(test1, "B").intValue(), 10)

    JS.setInstanceFieldValue(test1, "someNullValue", JS.getInstanceFieldValue(test1, "sampleClassInstance")); // class type
    assert(JS.getInstanceFieldValue(test1, "someNullValue").s.value, 's1')
    assert(JS.getClassName(JS.getInstanceFieldValue(test1, "someNullValue")), SAMPLE_CLASS)

    JS.setInstanceFieldValue(test1, "as", ['a', 'b', '1']); // js array
    const stringArr2 = JS.getInstanceFieldValue(test1, "as"); // arr type
    assert(stringArr2.isArray, true);
    assert(stringArr2.elemType, 'L' + STRING_CLASS + ';');
    assert(JS.getClassName(stringArr2), '[L' + STRING_CLASS + ';');
    assert(JS.toString(stringArr2), '["a","b","1"]');

    JS.setInstanceFieldValue(test1, "as", JS.newArray('L' + STRING_CLASS + ';', ['2', '3', '4'])); // Java.array
    const stringArr3 = JS.getInstanceFieldValue(test1, "as");
    assert(stringArr3.isArray, true);
    assert(stringArr3.elemType, 'L' + STRING_CLASS + ';');
    assert(JS.getClassName(stringArr3), '[L' + STRING_CLASS + ';');
    assert(JS.toString(stringArr3), '["2","3","4"]');

    JS.setInstanceFieldValue(test1, "as", JS.getInstanceFieldValue(test1, "ass")); // field value
    const stringArr4 = JS.getInstanceFieldValue(test1, "as");
    assert(stringArr4.isArray, true);
    assert(stringArr4.elemType, 'L' + STRING_CLASS + ';');
    assert(JS.getClassName(stringArr4), '[L' + STRING_CLASS + ';');
    assert(JS.toString(stringArr4), '["33","33","33"]');

    console.log("============================================== JS.setStaticFieldValue =========================================================")
    JS.setStaticFieldValue(TEST_CLASS, "si", 987)
    assert(JS.getStaticFieldValue(TEST_CLASS, "si"), 987)
    JS.setStaticFieldValue(TEST_CLASS, "si", 100)
    assert(JS.getStaticFieldValue(TEST_CLASS, "si"), 100)


    console.log("============================================== JS.callInstanceMethod =========================================================")
    assert(JS.callInstanceMethod(test1, 'overload', [3], ['int']), 3); // primitive type with param types
    assert(JS.callInstanceMethod(test1, 'overload', [3],), 3); // primitive type without param types

    const int1d = JS.callInstanceMethod(test1, 'getArr', ["hello"]); // returns 1d arr
    assert(int1d.isArray, true);
    assert(int1d.elemType, null);
    assert(JS.getClassName(int1d), null);
    assert(JS.toString(int1d), "[1,2,3]");

    const int2d = JS.callInstanceMethod(test1, 'getArr2', ["h"]); // returns 2d arr
    assert(JS.toString(int2d), "[[1],[2,3],[3]]");

    assert(JS.callInstanceMethod(test1, 'a1', [[999, 2, 1]]), 999); // raw arr as param
    assert(JS.callInstanceMethod(test1, 'a1', [JS.newArray('I', [555, 2, 1])]), 555); // Java.array as param
    assert(JS.callInstanceMethod(test1, 'a1', [JS.getInstanceFieldValue(test1, "aii")]), 1); // field value as param


    console.log("============================================== JS.callStaticMethod =========================================================")
    assert(JS.callStaticMethod(TEST_CLASS, 'sarrayFunc', [[1, 2, 3]], ['[I']), '1');


    console.log("============================================== Complex =========================================================")

    const arr = JS.newArray('I', JS.getInstanceFieldValue(test1, "aii")); // new array from field value
    assert(arr.isArray, true);
    assert(arr.elemType, 'I');
    assert(JS.getClassName(arr), '[I');
    assert(JS.toString(arr), "[1,2,3]");

    // new array from method value
    const arr2 = JS.newArray('[I', int2d); // new array from field value
    assert(arr2.isArray, true);
    assert(arr2.elemType, '[I');
    assert(JS.getClassName(arr2), '[[I');
    assert(JS.toString(arr2), "[[1],[2,3],[3]]");

    // new instance from field value
    const samplet = JS.newInstance(SAMPLE_CLASS, [JS.getInstanceFieldValue(test1, 'sampleClassInstance')])
    assert(JS.getClassName(samplet), SAMPLE_CLASS)
    assert(samplet.s.value, "sc")

    // new instance from method value
    const samplet2 = JS.newInstance(SAMPLE_CLASS, [JS.callInstanceMethod(test1, 'getSample')])
    assert(JS.getClassName(samplet2), SAMPLE_CLASS)
    assert(samplet2.s.value, "sc")

    // set instance field value from method value
    JS.setInstanceFieldValue(test1, "someNullValue", JS.callInstanceMethod(test1, 'getSample'));
    assert(JS.getInstanceFieldValue(test1, "someNullValue").s.value, 's1')
    assert(JS.getClassName(JS.getInstanceFieldValue(test1, "someNullValue")), SAMPLE_CLASS)
}
