// Entry point for the "Sum up 23 November's world news in one image" entry.
//
// The finished front page lives in entry.png beside this file. All this
// script does is place an exact copy of that image into the directory the
// harness asks for, so the judged artifact is always the file in this repo.
//
// Usage: node main.ts  (or: npx tsc / node with a TS runner)
//   MAKEFUN_OUTPUT_DIR   where entry.png should be written (default /output)

import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

if (!existsSync(source)) {
  throw new Error(`entry.png not found next to main.ts (${source})`);
}

mkdirSync(outDir, { recursive: true });
const destination = join(outDir, "entry.png");
copyFileSync(source, destination);
console.log(`entry.png -> ${destination}`);
