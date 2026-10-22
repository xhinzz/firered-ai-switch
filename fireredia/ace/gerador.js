// Roda o motor do CodeGenerator do E-Sh4rk (js_of_ocaml) fora do navegador.
// node gerador.js <ace_js.bc.js> <exit.txt> <lingua> <jogo> <codigo.txt>   -> imprime o resultado (nomes de caixa)
const fs = require("fs");
globalThis.self = globalThis;
const [motor, saidas, lingua, jogo, arquivo] = process.argv.slice(2);
const { aceGen } = require(motor);
const r = aceGen.build(lingua, jogo, fs.readFileSync(arquivo, "utf8"), fs.readFileSync(saidas, "utf8"));
console.log(r[1]);
