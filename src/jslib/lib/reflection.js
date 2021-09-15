import {primitiveTypeToWrapperType, typesToClasses} from "./types";
import {isEmpty} from "./utils";

export class Reflection {
    static getConstructorsOfClass(className) {
        const cls = Java.use(className);
        const constructors = cls.class.getDeclaredConstructors();
        return constructors;
    }

    static getFieldsOfClass(className) {
        const cls = Java.use(className);
        const fields = cls.class.getDeclaredFields();
        return fields;
    }

    static getMethodsOfClass(className) {
        const cls = Java.use(className);
        const methods = cls.class.getDeclaredMethods();
        return methods;
    }

    static getClassOfPrimitiveType(primitiveType) {
        const wrapperType = primitiveTypeToWrapperType(primitiveType);
        return JS.getStaticFieldValue(wrapperType, "TYPE");
    }

    static isStatic(fieldOrMethod) {
        const Modifier = Java.use("java.lang.reflect.Modifier");
        return Modifier.isStatic(fieldOrMethod.getModifiers())
    }


    static getDeclaredMethod(className, methodName, paramTypes) {
        let classes = null;
        if (!isEmpty(paramTypes)) {
            classes = typesToClasses(paramTypes);
        }

        const method = Java.use(className).class.getDeclaredMethod(methodName, classes);
        method.setAccessible(true);
        return method;
    }

    static getFieldValue(className, fieldName, instance = null) {
        const field = Reflection.getDeclaredField(className, fieldName);
        const value = field.get(instance);
        return value;
    }

    static getMethodReturnType(className, methodName, paramTypes) {
        const method = Reflection.getDeclaredMethod(className, methodName, paramTypes);
        return method.getReturnType().getName();
    }
}