import { expect, test } from 'vitest'
import { validIp } from '@/lib/ip'

test.each(['', '  ', '203.0.113.10', ' 203.0.113.10 ', '0.0.0.0', '255.255.255.255',
  '2001:db8::1', '::1', '::', '::ffff:192.0.2.1', '2001:db8:0:0:0:0:0:1'])(
  'accepts an address or an empty filter: %s', (ip) => expect(validIp(ip)).toBe(true),
)

test.each(['999.1.2.3', '01.2.3.4', '1', 'example.com', '1.2.3', '1.2.3.4:80',
  '<script>alert(1)</script>', '[::1]', '::1%eth0', '2001::db8::1', '2001:db8', '::ffff:192.168.001.1'])(
  'refuses a malformed address: %s', (ip) => expect(validIp(ip)).toBe(false),
)
