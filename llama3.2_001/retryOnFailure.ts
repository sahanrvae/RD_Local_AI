interface RetryOptions {
    maxAttempts?: number;
    sleepSeconds?: number;
}

function retryOnFailure<T>(
    func: () => Promise<T>,
    maxAttempts?: number,
    sleepSeconds?: number
): Promise<T> {
    for (let attempt = 0; attempt < maxAttempts; attempt++) {
        try {
            return func();
        } catch (error) {
            console.log(`Attempt ${attempt + 1} failed with error: ${error}`);
            await new Promise(resolve => setTimeout(resolve, sleepSeconds * 1000));
        }
    }
    throw new Error(`Failed after ${maxAttempts} attempts`);
}

// Usage:
const exampleFunction = async (): Promise<string> => {
    // simulate a failing function
    if (Math.random() < 0.5) {
        throw new Error('example error');
    } else {
        return 'success';
    }
};

retryOnFailure(exampleFunction).then(result => console.log(result));