let instancesCount = 1;
const instancesStore = {};

export const getInstance = (instanceId) => {
    const id = Number(instanceId);
    if (!(id in instancesStore)) {
        throw new Error("id (" + instanceId + ") doesn't exist in the store");
    }

    return instancesStore[id];
}

export const saveInstance = (instance) => {
    const instanceId = instancesCount;
    instancesCount++;
    instancesStore[instanceId] = instance;
    return instanceId;
}

export class ToJs {
    static Param(param) {
        if (param == null) {
            return null;
        }

        if (isJsArray(param)) {
            return ToJs.Params(param);
        }

        const paramData = JSON.parse(param);

        // if is an instance (also could by array instance), just get the instance
        if (paramData['id'] != null) {
            return getInstance(paramData['id']);
        }

        // it's a primitive type
        return paramData['value'];
    }

    static Params(params) {
        return params.map(p => ToJs.Param(p));
    }
}

export class ToPython {
    static Unknown(value) {
        if (isArrayHeuristic(value)) {
            value.isArray = true;
        }

        if (value != null && typeof (value) === 'object') {
            return ToPython.Instance(value, JS.getClassName(value));
        }

        return value;
    }

    static Instance(instance, className) {
        const id = saveInstance(instance);

        return {
            id,
            class_name: className,
            is_array: instance?.isArray
        }
    }

    static Class(className) {
        return {
            name: className
        }
    }

    static Constructor(className, constructor) {
        const paramTypes = constructor.getParameterTypes();
        const classNames = typesToClassNames(paramTypes);
        return {
            class_name: className,
            signature: constructor.toString(),
            param_types: classNames
        }
    }

    static Method(className, method) {
        const paramTypes = method.getParameterTypes();
        const classNames = typesToClassNames(paramTypes);
        return {
            class_name: className,
            name: method.getName(),
            signature: method.toString(),
            is_static: Reflection.isStatic(method),
            return_type: method.getReturnType().getName(),
            param_types: classNames
        }
    }

    static Field(className, field) {
        return {
            class_name: className,
            name: field.getName(),
            type: field.getType().getName(),
            declaration: field.toString(),
            is_static: Reflection.isStatic(field)
        }
    }
}

