### The purpose of this dir is to make the cpu code accessible in the browser with wasm
There are 2 ways to build, with wasm components or for pyodide.

1) for WASM components 
    (run from project root)
    compile to wasm
    `componentize-py -d web/wit -w cpuworld componentize web.cpu_module -o web/cpu_module.wasm`
    `componentize-py -d web/wit -w assembler componentize web.assembler_module -o web/assembler_module.wasm`
    transpile to js
    `jco transpile --no-namespaced-exports web/assembler_module.wasm -o web/assembler`
    `jco transpile --no-namespaced-exports web/cpu_module.wasm -o web/cpu`
    build
    `npm run build`
    `node main.js`

2) for pyodide wheel 
    run from `web/`
    `pip install wheel`
    `python setup.py bdist_wheel`
    `python -m http.server`
    visit localhost to view code in browser
