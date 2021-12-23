masm
model small
stack 512
assume cs: code, ds: data
data segment
    a db 5
    b db 3
    c db 2
    d db 8
data ends

code segment
main:
    mov ax, data
    mov ds, ax
    xor ax,ax
    mov al,a
    cbw
    mov bl,b
    mul bx
    mov dx, ax
    xor ax,ax
    xor bx,bx
    mov al, d
    mov bl, 8
    div bl
    add ax,dx
    xor bx,bx
    mov bl, 3
    sub ax, bx
    mov ax, 4c00h
    int 21h
    code ends
    end main


