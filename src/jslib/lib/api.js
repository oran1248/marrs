import {runTests} from "./tests";
import {Reflection} from "./reflection";
import {runInPromise} from "./utils";
import {getInstance, ToJs, ToPython} from "./proxy";
import {isArrayHeuristic} from "./types";

rpc.exports = {
    runTests() {
        return runInPromise(() => runTests());
    },
    runJs(code) {
        return runInPromise(() => {
            const res = eval(code);
            return ToPython.Unknown(res);
        })
    },
    disableHook(hookId) {
        return runInPromise(() => {
            JS.disableHook(hookId);
        })
    },
    enableHook(hookId) {
        return runInPromise(() => {
            JS.enableHook(hookId);
        })
    },
    hookMethod(...params) {
        return runInPromise(() => {
            JS.hookMethod(...params);
        })
    },
    getLoadedClasses(pattern) {
        return runInPromise(() => {
            const classes = JS.getLoadedClasses(pattern);
            return classes.map(c => ToPython.Class(c));
        });
    },
    getMethodsOfClass(className) {
        return runInPromise(() => {
            const methods = Reflection.getMethodsOfClass(className);
            return methods.map(m => ToPython.Method(className, m));
        });
    },
    getConstructorsOfClass(className) {
        return runInPromise(() => {
            const ctors = Reflection.getConstructorsOfClass(className);
            return ctors.map(c => ToPython.Constructor(className, c));
        });
    },
    getFieldsOfClass(className) {
        return runInPromise(() => {
            const fields = Reflection.getFieldsOfClass(className);
            return fields.map(f => ToPython.Field(className, f));
        });
    },
    getInstancesOfClass(className) {
        return JS.getAllInstancesOfClass(className).then(instances => {
            const res = [];
            for (const instance of instances) {
                res.push(ToPython.Instance(instance, className));
            }
            return res;
        });
    },
    getFieldValue(className, fieldName, instanceId) {
        return runInPromise(() => {
            let value;
            if (instanceId !== null) {
                const instance = getInstance(instanceId);
                value = JS.getInstanceFieldValue(instance, fieldName);
            } else {
                value = JS.getStaticFieldValue(className, fieldName);
            }

            return ToPython.Unknown(value);
        });
    },
    setFieldValue(className, fieldName, newValue, instanceId) {
        return runInPromise(() => {
            const jsNewValue = ToJs.Param(newValue);

            if (instanceId !== null) {
                const instance = getInstance(instanceId);
                JS.setInstanceFieldValue(instance, fieldName, jsNewValue);
            } else {
                JS.setStaticFieldValue(className, fieldName, jsNewValue);
            }
        });
    },
    createInstance(className, paramsDataJson) {
        return runInPromise(() => {
            const paramsData = JSON.parse(paramsDataJson);
            const {
                params,
                paramTypes
            } = paramsData;

            const jsParams = ToJs.Params(params);

            const instance = JS.newInstance(className, jsParams, paramTypes);
            return ToPython.Instance(instance, className);
        });
    },
    callMethod(methodName, paramsDataJson, instanceId, className) {
        return runInPromise(() => {
            const paramsData = JSON.parse(paramsDataJson);
            const {
                params,
                paramTypes
            } = paramsData;

            const jsParams = ToJs.Params(params);

            let value;
            if (instanceId !== null) {
                const instance = getInstance(instanceId);
                value = JS.callInstanceMethod(instance, methodName, jsParams, paramTypes);
            } else {
                value = JS.callStaticMethod(className, methodName, jsParams, paramTypes);
            }

            return ToPython.Unknown(value);
        });
    },
    toString(instanceId) {
        return runInPromise(() => {
            const instance = getInstance(instanceId);
            return JS.toString(instance);
        });
    },

    // arrays
    createArray(arrType, elems) {
        return runInPromise(() => {
            const arrElemType = arrType.substring(1);
            const jsElems = ToJs.Params(elems);

            const arr = JS.newArray(arrElemType, jsElems);
            return ToPython.Instance(arr, arrType);
        });
    },
    getArrayLength(instanceId) {
        return runInPromise(() => {
            const arr = getInstance(instanceId);

            if (!arr.isArray) {
                throw new Error("Instance is not an array");
            }

            return arr.length;
        });
    },
    arrayGetItem(instanceId, index) {
        return runInPromise(() => {
            const arr = getInstance(instanceId);

            if (!arr.isArray) {
                throw new Error("Instance is not an array");
            }

            const value = arr[index];

            if (isArrayHeuristic(value)) {
                value.isArray = true;
                value.source = 'getitem'
                value.elemType = JS.getClassName(arr)?.substring(1);
                value.$className = arr.elemType;
            }

            return ToPython.Unknown(value);
        });
    },
    arraySetItem(instanceId, index, value) {
        return runInPromise(() => {
            const arr = getInstance(instanceId);

            if (!arr.isArray) {
                throw new Error("Instance is not an array");
            }

            const jsValue = ToJs.Param(value);

            arr[index] = jsValue;

            // TODO: if arr.source === 'field' we can use reflection to change the original java array
            // const Array = Java.use("java.lang.reflect.Array");
            // Array.set(arr.javaRef, index, jsValue);
        });
    }
};
