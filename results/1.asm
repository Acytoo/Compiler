	.586
	.model flat, c

	.data
a	db	4 dup(0)
b	db	4 dup(0)
c	db	4 dup(0)
e	db	8 dup(0)

	.code

mov	c	10
mov	a	1
mov	a	11
mov	b	19.8
mov	b	9.879000000000001
CMP	8.9
JA	9
mov	b	10.44
mov	c	90
JMP	10
mov	c	80
d	db	4 dup(0)
CMP	80
JA	15
