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
