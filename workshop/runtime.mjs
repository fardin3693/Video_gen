// Print shell exports for npm-provided FFmpeg/ffprobe and serverless Chromium.
// Usage from repo root: eval "$(node workshop/runtime.mjs)"
// This prepares dependencies only; composition/rendering stays in HyperFrames.
import chromium from '@sparticuz/chromium';
import { createRequire } from 'node:module';
import { dirname, join, resolve } from 'node:path';
import { tmpdir } from 'node:os';
import { mkdirSync, readFileSync } from 'node:fs';
import { brotliDecompressSync } from 'node:zlib';
import { execFileSync } from 'node:child_process';
const require=createRequire(import.meta.url);
const root=resolve(dirname(new URL(import.meta.url).pathname),'..');
const browser=await chromium.executablePath();
const libs=join(tmpdir(),'hyperframes-chromium-libs');mkdirSync(libs,{recursive:true});
const bundled=join(root,'node_modules/@sparticuz/chromium/bin/al2023.tar.br');
execFileSync('tar',['-xf','-','-C',libs],{input:brotliDecompressSync(readFileSync(bundled))});
const ffmpeg=require('@ffmpeg-installer/ffmpeg').path;
const ffprobe=require('@ffprobe-installer/ffprobe').path;
const q=x=>"'"+x.replaceAll("'","'\\''")+"'";
console.log(`export HYPERFRAMES_BROWSER_PATH=${q(browser)}`);
console.log(`export LD_LIBRARY_PATH=${q(join(libs,'lib'))}:\${LD_LIBRARY_PATH:-}`);
console.log(`export PATH=${q(dirname(ffmpeg))}:${q(dirname(ffprobe))}:\"$PATH\"`);
