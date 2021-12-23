masm
model small
stack 256
assume cs: code, ds: data
data segment
    a db 8
    b db 4
    c db 6
    d db 6
    res1 db 0
    res10 db "00 $"
    res16 db "00h$"
data ends
code segment
main:
    mov ax, data
    mov ds, ax
    xor ax, ax

    mov al, a
    mov bl, b
    add ax, bx
    idiv c
    mov dl, d
    add al, dl
    xor bl, bl
    mov bl, 3
    add al, bl
    xor ah, ah 
    mov bl, 10
    mov si, 1
    mov res1, al


   decimal:                 ; перевод в десятичную
    div bl
    add ah, 48
    mov res10[si], ah
    xor ah, ah
    dec SI
    cmp al, 0
    jne decimal
    
mov ah, 9
mov dx, offset res10 
int 21h
    
xor ax, ax
mov al, res1
mov bl, 16
mov si, 1
    
hexdecimal:                 ; перевод в шестнадцатеричную
    div bl
    cmp ah, 10
    jge hexd 
    jl deci
        
deci:
    add ah, 48
    jmp fun
        
hexd: 
    add ah, 55
            
fun:
    mov res16[SI], AH
    xor ah, ah
    dec si
    cmp al, 0
    jne hexdecimal
    
mov ah, 9
mov dx, offset res16
int 21h 
 
mov ax, 4C00h
int 21h

    code ends
    end main

