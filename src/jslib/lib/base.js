import {isArrayHeuristic, isArrayType} from "./types";
import {isEmpty} from "./utils";


const preFieldCheck = (obj, fieldName) => {
    // check if field exists
    if (!(fieldName in obj)) {
        throw new Error("No such field '" + fieldName + "' in " + JS.toString(obj));
    }

    // check if fieldName is a function, if so, add "_" prefix
    if (typeof (obj[fieldName]) === "function") {
        fieldName = "_" + fieldName;
    }

    return fieldName;
}

const hooks = {};

export class JS {
    static disableHook(hookId) {
        hooks[hookId].enabled = false;
    }

    static enableHook(hookId) {
        hooks[hookId].enabled = true;
    }

    static hookMethod(hookId, className, methodName, paramTypes, getOriginalRetVal) {
        const cls = Java.use(className);
        const method = cls[methodName];

        hooks[hookId] = {
            enabled: true,
        };

        const implFunc = function (...runTimeParams) {
            // console.log("implFunc", runTimeParams)
            if (!hooks[hookId].enabled) {
                // console.log("calling original")
                // If hook is not enabled, just call the original method
                return method.call(this, ...runTimeParams);
            }

            hooks[hookId].method = method.bind(this);

            let originalRetVal = null;
            if (getOriginalRetVal) {
                originalRetVal = method.call(this, ...runTimeParams);
            }

            const pythonParams = runTimeParams.map(p => ToPython.Unknown(p));
            // console.log("pythonParams", pythonParams)
            send(JSON.stringify({
                type: 'hook-enter',
                hookId,
                params: pythonParams,
                originalRetVal
            }));

            let retVal = null;
            recv('continue@' + hookId, (data) => {
                // console.log("data", JSON.stringify(data))
                if (data?.payload?.retval != null) {
                    retVal = ToJs.Param(data.payload.retval);
                }
            }).wait();

            // console.log("retVal", retVal)
            return retVal;
        }


        if (!isEmpty(paramTypes)) {
            method.overload(...paramTypes).implementation = implFunc;
        } else {
            method.implementation = implFunc;
        }
    }

    static getAllInstancesOfClass(className) {
        return new Promise((resolve, reject) => {
            const instances = [];
            Java.choose(className, {
                onMatch: (instance) => {
                    instances.push(instance);
                },
                onComplete: () => {
                    resolve(instances);
                }
            });
        });
    }

    static getLoadedClasses(pattern) {
        const allClasses = JS.getAllLoadedClasses();
        const foundClasses = [];

        allClasses.forEach((cls) => {
            if (!pattern || cls.match(pattern)) {
                foundClasses.push(cls);
            }
        });

        return foundClasses;
    }

    static getAllLoadedClasses() {
        const allClasses = [];
        const classes = Java.enumerateLoadedClassesSync();

        classes.forEach((aClass) => {
            let className = aClass;

            const matches = className.match(/[L](.*);/);
            if (matches && matches.length >= 2) {
                className = matches[1].replace(/\//g, ".");
            }

            allClasses.push(className);
        });

        return allClasses;
    }

    static getClassName(jsWrapper) {
        return jsWrapper?.$className;
    }

    static toString(val) {
        if (val == null || val.isArray) {
            return JSON.stringify(val);
        }

        if (JS.getClassName(val) != null) {
            return val.toString();
        }

        return JSON.stringify(val);
    }

    static newArray(elemType, elems) {
        const arr = Java.array(elemType, elems)
        arr.isArray = true;
        arr.source = 'use';
        arr.elemType = elemType;
        arr.$className = '[' + elemType;
        return arr;
    }

    static callMethod(obj, methodName, params, paramTypes) {
        // check if method exists
        if (!(methodName in obj)) {
            throw new Error("No such method '" + methodName + "' in " + JS.toString(obj));
        }

        let res = null;
        if (!isEmpty(paramTypes)) {
            // console.log(obj[methodName].overload(...paramTypes).returnType.className);
            res = obj[methodName].overload(...paramTypes).call(obj, ...params);
        } else {
            res = obj[methodName](...params);
        }

        // TODO: find a way to identify that res is an array and what its type (if paramTypes != null it's easy)
        if (isArrayHeuristic(res)) {
            res.isArray = true;
            res.source = 'method'
            res.elemType = null;
            res.$className = null;
        }

        return res;
    }

    static getFieldValue(obj, fieldName) {
        fieldName = preFieldCheck(obj, fieldName);

        const value = obj[fieldName].value;
        const className = obj[fieldName]?._p?.[2]?.className;

        if (isArrayType(className)) {
            value.isArray = true;
            value.source = 'field'
            value.elemType = className.substring(1); // remove the first "["
            value.$className = className;
        }

        return value;
    }

    static callStaticMethod(className, methodName, params = [], paramTypes = null) {
        const cls = Java.use(className);
        return JS.callMethod(cls, methodName, params, paramTypes);
    }


    static callInstanceMethod(instance, methodName, params = [], paramTypes = null) {
        return JS.callMethod(instance, methodName, params, paramTypes);
    }

    static getStaticFieldValue(className, fieldName) {
        const cls = Java.use(className);
        return JS.getFieldValue(cls, fieldName);
    }

    static getInstanceFieldValue(instance, fieldName) {
        return JS.getFieldValue(instance, fieldName);
    }

    static setFieldValue(obj, fieldName, newValue) {
        // console.log(obj, JSON.stringify(obj), fieldName, newValue)
        fieldName = preFieldCheck(obj, fieldName);
        obj[fieldName].value = newValue;
    }

    static setStaticFieldValue(className, fieldName, newValue) {
        const cls = Java.use(className);
        JS.setFieldValue(cls, fieldName, newValue);
    }

    static setInstanceFieldValue(instance, fieldName, newValue) {
        JS.setFieldValue(instance, fieldName, newValue);
    }

    static newInstance(className, params = [], paramTypes = null) {
        const cls = Java.use(className);

        let res = null;
        if (!isEmpty(paramTypes)) {
            res = cls.$new.overload(...paramTypes).call(cls, ...params);
        } else {
            res = cls.$new(...params);
        }

        return res;
    }

}
