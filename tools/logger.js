#!/usr/bin/env node
const net = require('net');
const dgram = require('dgram');

function hexdump(buf) {
  const lines = [];
  for (let i = 0; i < buf.length; i += 16) {
    const chunk = buf.subarray(i, i + 16);
    const hex = Array.from(chunk).map(b => b.toString(16).padStart(2, '0')).join(' ');
    const ascii = Array.from(chunk).map(b => (b >= 32 && b < 127) ? String.fromCharCode(b) : '.').join('');
    lines.push(`${i.toString(16).padStart(4, '0')}  ${hex.padEnd(48)}  ${ascii}`);
  }
  return lines.join('\n');
}

function log(prefix, data, addr) {
  const ts = new Date().toISOString().slice(11, 23);
  const src = addr ? ` from ${addr}` : '';
  console.log(`\n[${ts}] ${prefix}${src} (${data.length} bytes)`);
  console.log(hexdump(data));
}

function startTcp(host, port) {
  const server = net.createServer(socket => {
    console.log(`\nTCP connection from ${socket.remoteAddress}:${socket.remotePort}`);
    socket.on('data', data => log('TCP recv', data, socket.remoteAddress));
    socket.on('close', () => console.log(`TCP connection closed by ${socket.remoteAddress}`));
  });
  server.listen(port, host, () => console.log(`TCP listening on ${host}:${port}`));
}

function startUdp(host, port) {
  const socket = dgram.createSocket('udp4');
  socket.on('message', (data, rinfo) => log('UDP recv', data, `${rinfo.address}:${rinfo.port}`));
  socket.bind(port, host, () => console.log(`UDP listening on ${host}:${port}`));
}

const [, , proto, portArg, hostArg] = process.argv;
if (!proto || !portArg) {
  console.log(`Usage: node ${require('path').basename(__filename)} <tcp|udp> <port> [bind-ip, default 192.168.0.70]`);
  process.exit(1);
}
const port = parseInt(portArg, 10);
const host = hostArg || '192.168.0.70';

if (proto === 'tcp') startTcp(host, port);
else if (proto === 'udp') startUdp(host, port);
else {
  console.log('protocol must be tcp or udp');
  process.exit(1);
}
