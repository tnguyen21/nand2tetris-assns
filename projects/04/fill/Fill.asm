// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

(MAIN)
@KBD
D=M
// if we see no input on kbd memory map, fill the screen white
@FILLWHITE
D;JEQ
// otherwise we fill the screen black
@FILLBLACK
0;JMP

(FILLBLACK)
// screen memory map is 32 words x 256 rows = 8192 words long
// we want to fill each word with wither 0 or -1
// init variables
@8192
D=A
@i
M=D
@SCREEN
D=A
// pointer ! 
@address
M=D
(LOOP_FILL_B)
// loop termination when i < 0
@i
D=M
@LOOP_FILL_B_END
D;JLT
// loop body
@address
A=M
M=-1
@i
M=M-1
@address
M=M+1
@LOOP_FILL_B
0;JMP
(LOOP_FILL_B_END)
@KBD
D=M
@MAIN
0;JMP

(FILLWHITE)
// init variables
@8192
D=A
@i
M=D
@SCREEN
D=A
@address
M=D

(LOOP_FILL_W)
// check if loop terminates
@i
D=M
@LOOP_FILL_W_END
D;JLT
// loop body
@address
A=M
M=0
@i
M=M-1
@address
M=M+1
@LOOP_FILL_W
0;JMP
(LOOP_FILL_W_END)
@KBD
D=M
@MAIN
0;JMP