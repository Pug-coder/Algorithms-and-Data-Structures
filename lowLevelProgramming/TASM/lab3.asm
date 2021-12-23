assume cs: code, ds: data

data segment
dummy db 0Dh, 0Ah, '$'
str1 db 100, 99 dup ('$')
str2 db 100, 99 dup ('$')
num db 100, 99 dup ('$')
a db "-1$"
b db "1$"
c db "0$"
err1 db "Error!$"

data ends

code segment

numconv:
	lea si, num+2
	mov bh, 10
	ps:	
		mov dl, [si]
		sub dl, 48
		add al, dl
		inc si
		mov bl, [si]
		cmp bl, 0Dh
		je exit
		mul bh

	exit:
		ret


strinput:
	mov ah, 0Ah
	int 21h
	
	mov dx, offset dummy
	mov ah, 09h
	int 21h
	ret
	
strncmp proc
	push bp
    mov bp, sp

    mov cl, [bp+8]
	mov si, [bp+4]
    mov di, [bp+6]
    mov al, [si]
    mov bl, [di]

    cmp al, cl
    jb error
    cmp bl, cl
    jb error

	compare:
		add si, 1
		add di, 1
	l:
		mov al, [si]
		mov bl, [di]
		inc si
		inc di
		mov dl, [si]
		cmp al, bl
		jne noteq
		loop l
	
	eqq:
		pop bp
		pop bx
		mov cx, offset c
		jmp endd

	noteq:
		cmp al, bl
		jb less
		jmp bigg
		
	less:
		pop bp
		pop bx
		mov cx, offset a
		jmp endd
		
	bigg:
		pop bp
		pop bx
		mov cx, offset b
		jmp endd

	error:
		xor ax, ax
		mov dx, offset err1
		mov ah, 09h
		int 21h
		mov ah, 4ch
		int 21h

	
	endd:
		push cx
		push bx
		ret
endp

start:
	mov ax, data
	mov ds, ax
	mov ax, 0
	
	lea dx, str1
	call strinput
	
	lea dx, str2
	call strinput
	xor ax, ax
	
	lea dx, num
	call strinput
	call numconv ;al == num
	xor ah, ah
	push ax

	lea si, str1+1
	lea di, str2+1
	push di
	push si

	call strncmp
	pop dx
	
	mov ah, 09h
	int 21h
	mov ah, 4ch
	int 21h

code ends
end start
