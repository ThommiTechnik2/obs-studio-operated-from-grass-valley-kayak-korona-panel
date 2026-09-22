# OBS Studio Bridge for Grass Valley Kayak/Korona Control Panel

Reverse-engineering a decommissioned Grass Valley/Thomson **Kayak DD-1** broadcast control panel to use it as a physical hardware controller for **OBS Studio** — key presses trigger scene changes and Macros/E-MEMs via the Advanced Scene Switcher plugin / obs-websocket v5

## Status

🚧 Early reverse-engineering phase — not yet functional. See [Plan](#plan) below.

## Hardware

- Panel: Grass Valley/Thomson "Kayak DD-1" Control Panel, model **CP RC3800**
- Internal board: "GRASS VALLEY GROUP PANEL CONTROLLER 2ME CTRPNL" (671-6533-xx) — CPLD + LVTH18512 parallel-bus drivers + key matrix (pads T37–T126)
- Note: the Kayak DD-1 is its own, lower-cost GV product line — **not** related in hardware/architecture to Kalypso/Zodiak/Kayenne. Only shares protocol heritage (Editor Protocol, Peripheral Bus II), not hardware.
- Rear connectors (confirmed by inspection):
  - RJ45/LAN — active
  - RS-232/COM1 — active
  - RS-485/COM2 — labeled "SPARE", unused
  - USB ×2 — labeled "SPARE", unused

## Key finding

Per the official *Kayak HD Installation Planning Guide*, the panel talks to its frame over **Ethernet** (CAT5/RJ45, TCP(UDP)/IP, 10/100Base-T) — not a proprietary serial bus:

- Default IPs: frame = `192.168.0.70`, panel = `192.168.0.73`
- Panel discovers its frame via a "Rescan" function in the Device Control menu
- Power: 48V DC, ≤1.3A (GV's own "KDD-PSU" supplies this for frame-less setups)

This shifted the project from hardware matrix-scanning (originally planned: a Teensy-based key-matrix scanner) to **network protocol reverse engineering**.

## Dead ends

- GV "Switcher Products — Protocols Manual" (covers Kalypso/Zodiak/Kayenne) does **not** document the DD-1/CP3800's internal panel bus — only external RS-422/RS-485 protocols
- RS-232 (COM1) is GPI trigger output only, not usable for key-press data
- The official *Kayak DD-1 Planning and Installation Manual* is not publicly downloadable (403 Forbidden on grassvalley.com)

## Plan

1. Power the panel with 48V DC (bench PSU with current limiting; verify connector pinout/polarity first)
2. Set a host NIC to `192.168.0.70/24` to simulate the frame
3. Capture the panel's connection attempt with Wireshark/tcpdump
4. Reconstruct the protocol (framing, handshake/heartbeat, key codes) from the captured bytes
5. Build a "fake frame" responder that keeps the panel happy and forwards key-press events to a host script driving Advanced Scene Switcher / obs-websocket v5

## Not included here

Proprietary Grass Valley firmware, installer software, and manuals are **not** published in this repository for copyright reasons.

## License

[Apache License 2.0](LICENSE.md)
