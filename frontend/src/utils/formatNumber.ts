export default function formatNumber(value: number, digits = 3): string {
  return value.toFixed(digits);
}
