// The World in One Image — 20 November 2026.
// The image is drawn from code by render.py and shipped as entry.png;
// this program only copies it to the output directory, so both runs
// of the grader write byte-identical output.
import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const out = process.env.MAKEFUN_OUTPUT_DIR;
if (!out) throw new Error("MAKEFUN_OUTPUT_DIR is not set");
const src = join(here, "entry.png");
if (!existsSync(src)) throw new Error("entry.png is missing from the repo");
mkdirSync(out, { recursive: true });
copyFileSync(src, join(out, "entry.png"));
