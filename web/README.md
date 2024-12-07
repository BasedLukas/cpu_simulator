This code is used in [on my blog]() to run the maze in the browser.
There are 2 ways to build, with wasm components or for pyodide.

for pyodide
run from `web/`
```
pip install wheel
python setup.py bdist_wheel
python -m http.server
```
visit localhost to view code in browser


for WASM components (not recommended)
(run from project root)

compile to wasm

`componentize-py -d web/wit -w emulator componentize web.emulator_module -o web/emulator.wasm`

transpile to js

`jco transpile --no-namespaced-exports web/emulator.wasm -o web/emulator`

build

`npm run build`
`node main.js`


