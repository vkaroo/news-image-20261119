import { existsSync, mkdirSync, readFileSync, statSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// Entry point for the news-image-20261119 bounty.
// The poster for Thursday 19 November 2026 is the file entry.png that
// sits next to this script. This program reads those exact bytes and
// writes them to the grader's output directory, so it needs no network
// and every run produces the same bytes.

const here = dirname(fileURLToPath(import.meta.url));
const sourcePath = join(here, "entry.png");

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });

if (!existsSync(sourcePath)) {
  console.error(`entry.png is missing next to main.ts: ${sourcePath}`);
  process.exit(1);
}

const bytes = readFileSync(sourcePath);
const destPath = join(outDir, "entry.png");
writeFileSync(destPath, bytes);

const written = statSync(destPath).size;
if (written !== bytes.length) {
  console.error(
    `size mismatch after write: read ${bytes.length} bytes, wrote ${written}`,
  );
  process.exit(1);
}
console.log(`Wrote ${destPath} (${written} bytes)`);
