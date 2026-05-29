/**
 * @typedef {Function} AsyncFunction
 * @param {...any} args
 * @returns {Promise<any>}
 */

/**
 * Executes an asynchronous function, retrying upon failure.
 *
 * @param {AsyncFunction} asyncFunc The async function to execute.
 * @param {number} [maxAttempts=3] The maximum number of times to attempt the call.
 * @param {number} [delayMs=1000] The delay in milliseconds between attempts.
 * @param {...any} args Arguments to pass to the async function.
 * @returns {Promise<any>} A promise that resolves with the function's result or rejects with the last error.
 */
async function retryOnFailure(asyncFunc, maxAttempts = 3, delayMs = 1000, ...args) {
    let lastError = null;

    for (let attempt = 1; attempt <= maxAttempts; attempt++) {
        try {
            console.log(`Attempt ${attempt}/${maxAttempts}...`);
            // Await the result of the asynchronous function
            return await asyncFunc(...args);
        } catch (error) {
            lastError = error;
            if (attempt < maxAttempts) {
                console.warn(`Attempt failed: ${error.message || error}. Retrying in ${delayMs / 1000} seconds...`);
                // Wait before the next attempt
                await new Promise(resolve => setTimeout(resolve, delayMs));
            } else {
                console.error("All attempts failed.");
                // Re-throw the last error after the loop finishes
                throw lastError;
            }
        }
    }
}

// Example Usage (Self-contained for demonstration)
let callCount = 0;
const unreliableServiceCall = async (...args) => {
    callCount++;
    if (callCount < 3) {
        throw new Error("Service unavailable");
    }
    return "Success after retries";
};

(async () => {
    try {
        const result = await retryOnFailure(unreliableServiceCall, 5, 500);
        console.log(`\nFinal Result: ${result}`);
    } catch (e) {
        console.error(`\nOperation failed permanently: ${e.message || e}`);
    }
})();