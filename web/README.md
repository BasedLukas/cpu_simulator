# run from project root:
`componentize-py -d web/wit -w cpuworld componentize web.cpu_module -o web/cpu_module.wasm`
`componentize-py -d web/wit -w assembler componentize web.assembler_module -o web/assembler_module.wasm`

`jco transpile --no-namespaced-exports web/assembler_module.wasm -o web/assembler`
`jco transpile --no-namespaced-exports web/cpu_module.wasm -o web/cpu`


`npm run build`
