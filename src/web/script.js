document.addEventListener('DOMContentLoaded', function() {
    const inputTextarea = document.getElementById('input');
    const submitBtn = document.getElementById('submit-btn');
    const runBtn = document.getElementById('run-btn');
    const debugOutput = document.getElementById('debug-output');
    const transpiledCode = document.getElementById('transpiled-code');
    const programOutput = document.getElementById('program-output');

    let currentJSCode = '';

    // Submit button click handler
    submitBtn.addEventListener('click', async function() {
        const code = inputTextarea.value.trim();
        
        if (!code) {
            debugOutput.textContent = 'Please enter some EmotiLang code.';
            debugOutput.className = 'error';
            return;
        }

        // Disable buttons during processing
        submitBtn.disabled = true;
        runBtn.disabled = true;
        submitBtn.textContent = 'Compiling...';

        // Clear previous outputs
        debugOutput.textContent = '';
        transpiledCode.textContent = '';
        programOutput.textContent = '';
        debugOutput.className = '';
        transpiledCode.className = '';
        programOutput.className = '';

        try {
            const response = await fetch('/compile', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ code: code })
            });

            const result = await response.json();

            if (result.success) {
                // Display debug output
                debugOutput.textContent = result.debug_output || 'Parsing successful!';
                
                // Display transpiled code
                transpiledCode.textContent = result.js_code || 'No JavaScript code generated.';
                currentJSCode = result.js_code || '';
                
                // Enable run button if we have JS code
                if (currentJSCode) {
                    runBtn.disabled = false;
                }
            } else {
                // Display error
                debugOutput.textContent = result.debug_output || 'Unknown error occurred';
                debugOutput.className = 'error';
                transpiledCode.textContent = result.error || 'Error in JavaScript code generation.';
                transpiledCode.className = 'error';
                currentJSCode = '';
                runBtn.disabled = true;
            }
        } catch (error) {
            debugOutput.textContent = 'Network error: ' + error.message;
            debugOutput.className = 'error';
            transpiledCode.textContent = '';
            currentJSCode = '';
        } finally {
            // Re-enable submit button
            submitBtn.disabled = false;
            submitBtn.textContent = 'Compile';
        }
    });

    // Run button click handler
    runBtn.addEventListener('click', function() {
        if (!currentJSCode) {
            programOutput.textContent = 'No code to run. Please compile first.';
            programOutput.className = 'error';
            return;
        }

        // Clear previous output
        programOutput.textContent = '';
        programOutput.className = '';

        // Capture console.log output
        const originalLog = console.log;
        const logs = [];
        
        console.log = function(...args) {
            logs.push(args.map(arg => 
                typeof arg === 'object' ? JSON.stringify(arg) : String(arg)
            ).join(' '));
            originalLog.apply(console, args);
        };

        try {
            // Create a safe execution environment
            const result = eval(`
                (function() {
                    ${currentJSCode}
                })()
            `);
            
            // Display captured logs
            if (logs.length > 0) {
                programOutput.textContent = logs.join('\n');
            } else if (result !== undefined) {
                programOutput.textContent = String(result);
            } else {
                programOutput.textContent = 'Code executed successfully (no output)';
            }
        } catch (error) {
            programOutput.textContent = 'Runtime Error: ' + error.message;
            programOutput.className = 'error';
        } finally {
            // Restore original console.log
            console.log = originalLog;
        }
    });

    // Allow Enter key to submit (Ctrl+Enter)
    inputTextarea.addEventListener('keydown', function(e) {
        if (e.ctrlKey && e.key === 'Enter') {
            submitBtn.click();
        }
    });
});
