import test from 'node:test';
import assert from 'node:assert/strict';
import { nextScrollTop } from './policy.mjs';

const variant = process.env.SCROLL_VARIANT ?? 'fixed';
test('idle content keeps its position across ten timer ticks', () => {
  let position = 120;
  for (let i = 0; i < 10; i++) position = nextScrollTop(position, { type: 'tick' }, variant);
  assert.equal(position, 120);
});
test('manual wheel down still moves the content', () => {
  assert.equal(nextScrollTop(120, { type: 'wheel', delta: 80 }, variant), 200);
});
test('manual wheel up still moves the content', () => {
  assert.equal(nextScrollTop(120, { type: 'wheel', delta: -60 }, variant), 60);
});
test('manual scrolling cannot move above the beginning', () => {
  assert.equal(nextScrollTop(20, { type: 'wheel', delta: -80 }, variant), 0);
});
