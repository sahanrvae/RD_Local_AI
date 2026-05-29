/**
 * Executes an asynchronous function, retrying upon failure.
 *
 * @template T The return type of the successful function call.
 * @template A The type of the function arguments.
 * @param {async (...args: A) => Promise<T>} asyncFunc The async function to execute.
 * @param {number} [maxAttempts=3] The maximum number of times to attempt the call.
 * @param {number} [delayMs=1000] The delay in milliseconds between attempts.
 * @param {...A} args Arguments to pass to the async function.
 * @returns {Promise<T>} A promise that resolves with the function's result or rejects with the last error.
 */
async function retryOnFailure<T, A extends any[]>(
    asyncFunc: (...args: A) => Promise<T>,
    maxAttempts: number = 3,
    delayMs: number = 1000,
    ...args: A
): Promise<T> {
    let lastError: Error | any = null;

    for (let attempt = 1; attempt <= maxAttempts; attempt++) {
        try {
            console.log(`Attempt ${attempt}/${maxAttempts}...`);
            // Await the result of the asynchronous function
            return await asyncFunc(...args);
        } catch (error) {
            lastError = error instanceof Error ? error : new Error(String(error));

            if (attempt < maxAttempts) {
                console.warn(`Attempt failed: ${lastError.message}. Retrying in ${delayMs / 1000} seconds...`);
                // Wait before the next attempt
                await new Promise(resolve => setTimeout(resolve, delayMs));
            } else {
                console.error("All attempts failed.");
                // Re-throw the last error after the loop finishes
                throw lastError;
            }
        }
    }
    // This line is technically unreachable if maxAttempts >= 1, but satisfies typescript compiler
    throw lastError || new Error("Unknown failure"); 
}

// Example Usage (Self-contained for demonstration)
let callCountTS = 0;
const unreliableServiceCallTS = async (...args: any[]): Promise<string> => {
    callCountTS++;
    if (callCountTS < 3) {
        throw new Error("Service unavailable");
    }
    return "Success after retries";
};

(async () => {
    try {
        const result = await retryOnFailure(unreliableServiceCallTS, 5, 500);
        console.log(`\nFinal Result: ${result}`);
    } catch (e) {
        console.error(`\nOperation failed permanently: ${(e as Error).message || e}`);
    }
})();