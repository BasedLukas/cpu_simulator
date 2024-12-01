import resolve from "@rollup/plugin-node-resolve";
import commonjs from "@rollup/plugin-commonjs";
import copy from "rollup-plugin-copy";

export default {
    input: "main.js", // Entry file
    output: {
        file: "dist/bundle.js", // Output file for the browser
        format: "es", // Use ES module format
    },
    plugins: [
        resolve(), // Resolve Node.js modules
        commonjs(), // Convert CommonJS modules to ES modules
        copy({
            targets: [
                { src: "cpu/*.wasm", dest: "dist" }, // Copy .wasm files to dist
                { src: "assembler/*.wasm", dest: "dist"}
            ],
        }),
    ],
};
