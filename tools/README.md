# Kayak HD Panel — Protocol Discovery

Diagnostic tools to figure out what the CP3800/DD-1 control panel actually
sends over its RJ45 link, now that we know it speaks TCP(UDP)/IP to the
frame (default IPs: frame `192.168.0.70`, panel `192.168.0.73`).

These scripts do **not** know the protocol yet — nobody does. They're just
generic listeners that log every raw byte they receive, so we can look at
the hex dumps and work out the protocol from there.

## Step 0 — give your machine the frame's IP

Connect your laptop directly to the panel via RJ45 (or through a switch),
then give your machine `192.168.0.70/24` as an address on that interface —
this makes the panel treat you as "the frame" for ARP/connection purposes.

macOS example (adjust `en7` to your actual interface from `ifconfig`):

```bash
sudo ifconfig en7 alias 192.168.0.70/24
```

## Step 1 — pure discovery, no script needed yet

Before running any of the scripts below, just capture with Wireshark or
`tcpdump` and power on the panel:

```bash
sudo tcpdump -i en7 -n -X host 192.168.0.73
```

Look for the panel's connection attempts (TCP SYN packets, or UDP packets)
to `192.168.0.70` — the destination **port number** in that capture tells
you what to point the logger scripts at next. Also note whether it's
TCP or UDP.

## Step 2 — log whatever the panel sends on that port

Python (stdlib only, no install needed):

```bash
sudo python3 logger.py tcp 5253 192.168.0.70
```

Node (stdlib only, no install needed):

```bash
sudo node logger.js tcp 5253 192.168.0.70
```

(`5253` above is a placeholder — replace with the real port from Step 1.
`sudo` is only required if the port is below 1024.)

Both scripts print a timestamped hex+ASCII dump of every packet/connection
they see. If it's TCP, the panel may just get a connection accepted with no
reply and then send its data — capture a few button presses and share the
hex dumps so we can start decoding the message structure (framing, length
bytes, checksums, key codes).

## Next step after this

Once we understand a few message types (at minimum: whatever handshake the
panel expects to consider itself "linked", plus one button-press message),
we extend one of these scripts into an actual frame emulator that replies
correctly and forwards decoded button events into the OBS/Advanced Scene
Switcher bridge.
