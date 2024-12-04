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
    pyodide.runPythonAsync(await fetchDocumentAsString('main.py'));
    document.getElementById("solutionButton").addEventListener("click", () => {
        document.getElementById("assemblyCode").value = pyodide.globals.get("solution_code");
    });
    document.getElementById('output').innerText = 'Loaded';
    // once loaded show maze
    document.getElementById('loadingIndicator').style.display = 'none';
    document.getElementById('mazeCanvas').style.display = 'block';

}
main()
