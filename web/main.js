import {cpuinit} from "./cpu/cpu_module.js";
import {assemblebinary} from "./assembler/assembler_module.js";

console.log(cpuinit);
const program = assemblebinary("7\ncopy 0 1\ncopy 1 6");
console.log(program)
const output = cpuinit(program);
console.log(output);
// window.cpu = cpuinit;
// window.ab = assemblebinary;
