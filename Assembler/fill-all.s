SUB r1, r1, #1
main: ADD r1, r1, #1
ADD r14, r15, #2
BIM draw
CMP r1, #15
BNE main
MOV r1, #0
SUB r1, r1, #1
ADD r0, r0, #1
BIM main
draw: STR r0, #0xFFFC
STR r1, #0xFFFD
MOV r2, #3
STR r2, #0xFFFE
B r14
