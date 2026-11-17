import { spawnSync } from 'node:child_process';
import { readFileSync, writeFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';

const cwd = fileURLToPath(new URL('.', import.meta.url));
const expectations = {
  buggy: ['idle content keeps its position across ten timer ticks'],
  overfixed: [
    'manual wheel down still moves the content',
    'manual wheel up still moves the content',
    'manual scrolling cannot move above the beginning',
  ],
  fixed: [],
};
const results = [];
for (const [variant, expectedFailures] of Object.entries(expectations)) {
  const result = spawnSync(process.execPath, ['--test', '--test-reporter=tap', 'acceptance.test.mjs'], {
    cwd, encoding: 'utf8', env: { ...process.env, SCROLL_VARIANT: variant }, timeout: 15000,
  });
  const output = result.stdout ?? '';
  const failures = [...output.matchAll(/^not ok \d+ - (.+)$/gm)].map(match => match[1]);
  const count = Number(output.match(/^# tests (\d+)$/m)?.[1]);
  const expectedExit = expectedFailures.length ? 1 : 0;
  if (result.error || result.status !== expectedExit || count !== 4 ||
      JSON.stringify(failures) !== JSON.stringify(expectedFailures)) {
    console.error(output, result.stderr ?? '', result.error ?? '');
    throw new Error(`Unexpected acceptance result for ${variant}`);
  }
  results.push({ variant, tests: count, passed: count - failures.length, failed: failures.length, failures });
  console.log(`${variant}: ${count - failures.length}/${count} pass; ${failures.length} expected failures`);
}
if (process.argv.includes('--record')) {
  const digest = name => createHash('sha256').update(readFileSync(new URL(name, import.meta.url))).digest('hex');
  writeFileSync(new URL('evidence.json', import.meta.url), JSON.stringify({
    observed_at: new Date().toISOString(), runtime: process.version,
    command: 'node examples/scroll-drift/verify.mjs --record',
    scope: 'JavaScript policy acceptance tests; not a Claude session or an automated browser test',
    policy_sha256: digest('policy.mjs'), tests_sha256: digest('acceptance.test.mjs'), results,
  }, null, 2) + '\n');
}
