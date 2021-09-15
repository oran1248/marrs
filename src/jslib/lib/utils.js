export const isEmpty = (arr) => {
    return arr == null || arr.length === 0;
}

export const runInPromise = (func) => {
    return new Promise((resolve, reject) => {
        Java.perform(() => {
            try {
                const result = func();
                resolve(result);
            } catch (e) {
                reject(e);
            }
        });
    });
}

