// Box.asm  -  K = 67
//   While any key is pressed, draw a black box; when released, erase it.
//   Box: starts at row 67, 20 rows tall,
//        16 * ((67 mod 4) + 1) = 16 * 4 = 64 pixels wide = 4 words, from left edge.
//   First word of row 67 = SCREEN + 32*67 = 16384 + 2144 = 18528
//
// Variables: color (RAM[16]), addr (RAM[17]), rows (RAM[18])

(LOOP)
    @KBD
    D=M
    @DRAW
    D;JNE           // key pressed -> draw black
    @color
    M=0             // no key -> paint white (erase)
    @PAINT
    0;JMP
(DRAW)
    @color
    M=-1            // all 16 bits set = black
(PAINT)
    @18528          // SCREEN + 32*67
    D=A
    @addr
    M=D
    @20             // 20 rows
    D=A
    @rows
    M=D
(ROWLOOP)
    @color
    D=M
    @addr
    A=M
    M=D             // word 0 of this row
    A=A+1
    M=D             // word 1
    A=A+1
    M=D             // word 2
    A=A+1
    M=D             // word 3  (4 words = 64 pixels)
    @addr
    D=M
    @32
    D=D+A
    @addr
    M=D             // next row (+32 words)
    @rows
    M=M-1
    D=M
    @ROWLOOP
    D;JGT
    @LOOP
    0;JMP
