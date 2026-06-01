const retryOnFailure = async function (func, maxAttempts = 3, sleepSeconds = 1.0) {
    for (let attempt = 0; attempt < maxAttempts; attempt++) {
        try {
            const result = await func();
            return result;
        } catch (error) {
            console.log(`Attempt ${attempt + 1} failed with error: ${error}`);
            await new Promise(resolve => setTimeout(resolve, sleepSeconds * 1000));
        }
    }
    throw new Error(`Failed after ${maxAttempts} attempts`);
};

// Usage:
const exampleFunction = async () => {
    // simulate a failing function
    if (Math.random() < 0.5) {
        throw new Error('example error');
    } else {
        return 'success';
    }
};

retryOnFailure(exampleFunction).then(result => console.log(result));