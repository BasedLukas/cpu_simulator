### The purpose of this dir is to make the cpu code accessible in the browser with wasm
There are 2 ways to build, with wasm components or for pyodide.


1) for pyodide wheel 
    run from `web/`
    `pip install wheel`
    `python setup.py bdist_wheel`
    `python -m http.server`
    visit localhost to view code in browser


2) for WASM components 
    (run from project root)
    compile to wasm
    `componentize-py -d web/wit -w emulator componentize web.emulator_module -o web/emulator.wasm`
    transpile to js
    `jco transpile --no-namespaced-exports web/emulator_module.wasm -o web/emulator`
    build
    `npm run build`
    `node main.js`


