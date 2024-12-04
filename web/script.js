async function fetchDocumentAsString(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const text = await response.text();
        return text;
    } catch (error) {
        console.error('Error fetching document:', error);
        throw error;
    }
}

async function main() {
    let pyodide = await loadPyodide();
    await pyodide.loadPackage("micropip");
    document.getElementById('output').innerText = 'Pyodide loaded. Installing package...';

    // Load and run the initialization Python code
    await pyodide.runPythonAsync(await fetchDocumentAsString('main.py'));


    // Expose the run_game function to JavaScript
    const run_game = pyodide.globals.get('run_game');
    const stop_game = pyodide.globals.get('stop_game');

    // Add event listeners to the buttons
    document.getElementById('runButton').addEventListener('click', () => {
        run_game();
    });

    document.getElementById('stopButton').addEventListener('click', () => {
        stop_game();
    });
}
main();
