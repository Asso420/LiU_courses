
MENU:

	push	r16
	
	ldi		ZH, HIGH(MENU_SCR)
	ldi		ZL, LOW(MENU_SCR)
	call	ERASE_VMEM

	ldi		r16, $3C
	sts		MENU_SCR+6, r16
	sts		MENU_SCR+3, r16
	sts		MENU_SCR, r16
	ldi		r16, $20
	sts		MENU_SCR+4, r16
	sts		MENU_SCR+5, r16
	ldi		r16, $4
	sts		MENU_SCR+2, r16
	sts		MENU_SCR+1, r16
MENU_CONTINUE:
	sbic	PIND, START_BUTTON
	rjmp	MENU_CONTINUE
/*	ldi		ZH, HIGH(MENU_SCR)
	ldi		ZL, LOW(MENU_SCR)
	call	ERASE_VMEM*/
	ldi		ZH, HIGH(MENU_SCR)
	ldi		ZL, LOW(MENU_SCR)
	ldi		r16, 8
	call	ERASE_VMEM
	pop		r16
	ret