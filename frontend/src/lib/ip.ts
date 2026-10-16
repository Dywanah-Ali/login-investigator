export const IP_ERROR = 'That is not a valid IP address. Clear the box or enter one like 203.0.113.10.'

/** Empty means all. Keep the original spelling because the core matches IPs exactly. */
export function validIp(value: string | undefined): boolean {
  const ip = value?.trim() ?? ''
  if (!ip) return true
  if (!ip.includes(':')) return ipv4(ip)
  if (!/^[0-9a-f:.]+$/i.test(ip)) return false
  if (ip.includes('.') && !ipv4(ip.slice(ip.lastIndexOf(':') + 1))) return false
  try {
    // The browser's URL parser validates the bracketed IPv6 address without making a request.
    new URL(`http://[${ip}]/`)
    return true
  } catch {
    return false
  }
}

function ipv4(ip: string): boolean {
  const parts = ip.split('.')
  return parts.length === 4 && parts.every((part) => /^(0|[1-9]\d{0,2})$/.test(part) && Number(part) <= 255)
}
