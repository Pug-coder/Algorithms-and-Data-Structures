assume CS:code, DS: data
DATA SEGMENT
a DW ?
b DW ?
c DW ?
d DW ?
DATA ENDS

CODE SEGMENT
    START:
    ; (a + b) / c + d + 3
    MOV AX, 2
    MOV BX, 3
    MOV CX, 4
    MOV DX, 5
    ADD AX, BX
    XCHG AX, CX
    IDIV CX
    ADD CX, DX
    ADD CX, 3
CODE ENDS
END
