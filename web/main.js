import {assemblebinary, cpuinit,} from "./emulator/emulator.js";

console.log(cpuinit);
const program = assemblebinary("7\ncopy 0 1\ncopy 1 6");
console.log(program)
const output = cpuinit(program);
console.log(output);
// window.cpu = cpuinit;
// window.ab = assemblebinary;
