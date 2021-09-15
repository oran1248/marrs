import {Reflection} from "./reflection";

const primitiveTypeToWrapperMap = {
    byte: 'java.lang.Byte',
    short: 'java.lang.Short',
    int: 'java.lang.Integer',
    long: 'java.lang.Long',
    float: 'java.lang.Float',
    double: 'java.lang.Double',
    boolean: 'java.lang.Boolean',
    char: 'java.lang.Character',
}

const primitiveTypes = [
    'byte', 'short', 'int', 'long', 'float', 'double', 'boolean', 'char'
]


export const isArrayType = (cls) => {
    return cls != null && cls.startsWith("[");
}

export const isJsArray = (val) => {
    return val?.constructor === Array;
}

export const isArrayHeuristic = (val) => {
    if (val == null) {
        return false;
    }

    if (isJsArray(val)) {
        return true;
    }

    if (typeof (val) !== 'object') {
        return false;
    }

    if (!('length' in val)) {
        return false;
    }

    const length = val.length;

    if (typeof (length) !== 'number') {
        return false;
    }

    const keys = Object.keys(val);

    if (length !== keys.length - 1) {
        return false;
    }

    for (let i = 0; i < length; i++) {
        if (!(i in val)) {
            return false;
        }
    }

    return true;
}

const isPrimitiveType = (cls) => {
    return primitiveTypes.includes(cls);
}

export const getClassOfType = (typeName) => {
    if (isPrimitiveType(typeName)) {
        return Reflection.getClassOfPrimitiveType(typeName);
    }

    return Java.use(typeName).class;
}

export const typesToClasses = (types) => {
    const classes = [];
    for (const t of types) {
        classes.push(getClassOfType(t));
    }
    return classes;
}

export const typesToClassNames = (types) => {
    const classes = []
    for (const t of types) {
        classes.push(t.getName());
    }
    return classes;
}

export const primitiveTypeToWrapperType = (primitiveType) => {
    return primitiveTypeToWrapperMap[primitiveType];
}
