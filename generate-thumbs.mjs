import sharp from 'sharp';
import { readdir, mkdir } from 'fs/promises';
import { join } from 'path';

const SRC = 'public/images/gallery';
const DEST = 'public/images/gallery/thumbs';
const THUMB_WIDTH = 400;
const QUALITY = 75;

async function run() {
  await mkdir(DEST, { recursive: true });

  const files = (await readdir(SRC)).filter(f => f.endsWith('.jpg'));
  console.log(`Generating ${files.length} thumbnails (${THUMB_WIDTH}px wide, WebP q${QUALITY})...`);

  let done = 0;
  const BATCH = 20;

  for (let i = 0; i < files.length; i += BATCH) {
    const batch = files.slice(i, i + BATCH);
    await Promise.all(batch.map(async (file) => {
      const src = join(SRC, file);
      const dest = join(DEST, file.replace('.jpg', '.webp'));
      try {
        await sharp(src)
          .resize({ width: THUMB_WIDTH, withoutEnlargement: true })
          .webp({ quality: QUALITY })
          .toFile(dest);
        done++;
      } catch (e) {
        console.error(`Failed: ${file}`, e.message);
      }
    }));
    process.stdout.write(`\r  ${done}/${files.length}`);
  }

  console.log('\nDone!');

  // Check size reduction
  const { statSync } = await import('fs');
  let origTotal = 0, thumbTotal = 0;
  for (const file of files) {
    origTotal += statSync(join(SRC, file)).size;
    try {
      thumbTotal += statSync(join(DEST, file.replace('.jpg', '.webp'))).size;
    } catch {}
  }
  console.log(`Original: ${(origTotal / 1024 / 1024).toFixed(1)} MB`);
  console.log(`Thumbs:   ${(thumbTotal / 1024 / 1024).toFixed(1)} MB`);
  console.log(`Reduction: ${((1 - thumbTotal / origTotal) * 100).toFixed(0)}%`);
}

run();
