# Hack Capstone - K = 67

| Item | Value |
|---|---|
| K | 67 (last two digits of roll no. 2501350067) |
| Box start row | 67 |
| Box height | 20 rows (rows 67-86) |
| Box width | 16 x ((67 mod 4) + 1) = 16 x 4 = **64 pixels = 4 words** |
| First word address | SCREEN + 32*67 = 18528 |
| Extra feature | 67 mod 3 = 1 -> error message with line number instead of crashing |

## Folder layout (copy into your lab repo as `capstone/`)
- hdl/CPU.hdl, hdl/Memory.hdl, hdl/Computer.hdl  (Part A)
- assembler.py                                   (Part B)
- Box.asm, Box.hack                              (Part C)
- asm_tests/                                     (Add, Max, Rect + Bad.asm for the extra feature)

## Part A - how to test (Hardware Simulator)
Put CPU.hdl / Memory.hdl / Computer.hdl in the same folder as your older chips
(And, Or, Not, Mux16, DMux, ALU, ARegister/DRegister, PC, RAM16K ...) and the official
CPU.tst, Memory.tst, ComputerAdd.tst, ComputerMax.tst, ComputerRect.tst + .cmp files.
If an older chip fails, delete your file so the built-in is used, and say so in the report.
Screenshot each "End of script - Comparison ended successfully".

## Part B - run
    python3 assembler.py asm_tests/Add.asm      # compare with official assembler output
    python3 assembler.py Box.asm                # makes Box.hack
Test Pong.asm yourself too (download from the official project 6 files) and diff against the official .hack.

## Part C - run
CPU Emulator -> Load Program -> Box.hack -> Run, then click the screen and hold a key.
Take a screenshot while the key is held (black box at row 67, 64px wide).
