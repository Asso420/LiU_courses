MOVE:
	push	ZH
	push	ZL
	push	r18
	push	r17
	push	r16
	in		r16, SREG
	push	r16	
	lds		r18, MOV_DIR
	cpi		r18, $00
	breq	MOVE_W
	cpi		r18, $03
	breq	MOVE_N
	cpi		r18, $01
	breq	MOVE_E
	cpi		r18, $02
	breq	MOVE_N
	jmp		MOVE_DONE
	
MOVE_N:
	lds		r17, PPOS_Y
	cpi		r17, 7
	brne	CONTINUE_MOVE
LIMITS:
	clr		r17
	sts		SNAKE+7, ZERO_REG
	jmp		COLD
CONTINUE_MOVE:
	ldi		ZH, HIGH(SNAKE)
	ldi		ZL, LOW(SNAKE)
	add		ZL, r17
	ld		r16, Z
	st		Z+, ZERO_REG
	st		Z+, r16
	inc		r17
	sts		PPOS_Y, r17
	jmp		MOVE_DONE

MOVE_W: ;Move west
	lds		r18, PPOS_Y
	ldi		ZH, HIGH(SNAKE)
	ldi		ZL, LOW(SNAKE)
	add		ZL, r18
	ld		r16, Z
	rol		r16
	cpi		r16, $00
	breq	DEAD				//Respawnar skiten
	sts		SNAKE, r16
	jmp		MOVE_DONE
MOVE_E: ;Move west
	lds		r18, PPOS_Y
	ldi		ZH, HIGH(SNAKE)
	ldi		ZL, LOW(SNAKE)
	add		ZL, r18
	ld		r16, Z
	rol		r16
	cpi		r16, $00
	breq	DEAD				//Respawnar skiten
	sts		SNAKE, r16
	jmp		MOVE_DONE
DEAD:
	ldi		r16, $01
	sts		SNAKE, r16
MOVE_DONE:
	pop		r16
	out		SREG, r16
	pop		r16
	pop		r17
	pop		r18
	pop		ZL
	pop		ZH
	reti