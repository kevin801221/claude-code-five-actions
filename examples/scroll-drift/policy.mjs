/** The broken variants are intentional teaching fixtures. */
export function nextScrollTop(position, event, variant = 'fixed') {
  if (!['buggy', 'overfixed', 'fixed'].includes(variant)) throw new Error('Unknown variant');
  if (variant === 'overfixed') return position;
  if (event.type === 'tick') return variant === 'buggy' ? position + 1 : position;
  if (event.type === 'wheel') return Math.max(0, position + event.delta);
  return position;
}
