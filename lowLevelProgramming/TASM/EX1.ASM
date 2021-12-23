masm
model small
stack 256
assume cs: code, ds: data
data segment
    a db 8
    b db 4
    c db 6
    d db 2
data ends
code segment
main:
    mov ax, data
        mov ds, ax
        xor ax, ax
        mov al, a
        cbw
        mov bl, b
        add ax, bx
        idiv c
        mov dl, d
        add al, dl
        xor bl, bl
        mov bl, 3
        add al, bl
        xor dl, dl
        mov dl, 10
        mov ah, 2h
        int 21h
        mov dl, 13
        int 21h
        xor ax, ax
        mov al, a
        aam
        add ax, 3030h
        mov dl,ah
        mov dh, al
        mov ah, 02
        int 21h
        mov dl, dh
        int 21h

        mov ax, 4c00h
        int 21h
        code ends
        end main
