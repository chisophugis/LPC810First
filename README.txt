Bare metal communication with LPC810

Literally it is just a DIP-8 LPC810 on a breadboard with a UART
interface to my PC. (and a little bit of power stuff)

IIRC I mostly did this because I wanted to get an idea of bare-metal
booting of a chip.
This is my usual approach to things: do a minimal toy thing at the
"lowest level" (that term is context-dependent).
Even if it barely works, simply having "broken the ice" is 80% of the
learning experience.
This has a ton of benefits.
Mainly it gives a better understanding/appreciation of the existing
tooling.
It also really helps debug certain things to have done a "low-level"
experiment like this.
It also gives confidence that if I needed to go further and e.g.
bring up a whole toolchain then I could do that.
I.e., once something end-to-end is working, incrementally growing that
out to something full-blown is just "hard work" with limited "unknown
unknowns".
The "breaking the ice" is where the "unknown unknowns" are dispelled
and new capabilities are added to my list of "things I can juggle
around and piece together when trying to accomplish something".


Useful documents:

"UM10601 LPC81x User manual"
  - from NXP
  - family info
  - see especially "21.6.2 Boot process"
"LPC81xM 32-bit ARM Cortex-M0+ microcontroller; up to 16 kB flash and
4 kB SRAM"
  - from NXP
  - device-specific datasheet
"ARMv6-M Architecture Reference Manual"
  - from ARM (ARM DDI0419C)
  - see especially instruction encoding stuff
"Cortex-M0+ Technical Reference Manual"
  - from ARM (ARM DDI 0484B)
  - don't remember if I looked at this much.
