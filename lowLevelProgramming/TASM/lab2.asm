assume cs: code, ds: data

data segment
	a db 1,3,-5,5, 3,1,-16,1	; result = 3
	n equ 8
	msg db "0$"
data ends

code segment
start:
	mov ax, data
	mov ds, ax
	mov ax, 0
	mov dl, a[0]
	mov si, 1


	iterate:						; проход по массиву
		cmp a[si], dl
		jnl count
		mov dl, a[si]
		inc si
		cmp si, n
		je help
		jmp iterate
		
	count:						; счетчик
		inc ax
		mov dl, a[si]
		inc si
		cmp si, n
		je help
		jmp iterate
	
	help:
		mov bl, 10
		mov si, 0 
		
	decimal:					; вывод
		div bl
		add ah, 48
		mov msg[si], ah
		xor ah, ah
		dec si
		cmp al, 0
		jne decimal
		
	mov ah, 9
	mov dx, offset msg 
	int 21h
	
	mov ax, 4C00h
	int 21h

code ends
end start
