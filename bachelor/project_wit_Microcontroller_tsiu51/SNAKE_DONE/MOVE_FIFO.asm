 
MOVE_MAIN:
	push	ZH
	push	ZL
	push	r16
	push	r17
	push	r18
	push	r19
	push	r20
	in		r16, SREG
	push	r16

	//CHECKS AND CHANGES POSITION OF SNAKE HEAD
	;cli
	call	CHECK_DIR
	call	FIFO_PUSH		;IN(r20) NEW HEAD POS
	call	FIFO_POP		;OUT(r20) HEAD POS

	call	SET_PIX			;IN=r20, OUT=r19(X) r16(Y)
	;call	CHECK_HIT		;CMP r20(head pos) with FOOD_POS
	call	UPDATE_SNAKE	;SNAKE_FIFO -> SNAKE
	call	CHECK_HIT		;CMP r20(head pos) with FOOD_POS
	
	pop		r16
	out		SREG, r16
	pop		r20
	pop		r19
	pop		r18
	pop		r17
	pop		r16
	pop		ZL
	pop		ZH
	reti ;;;;;;;;;;;;Reti


//CHECKING JOYSTICK DIRECTION AND MOVING ACCORDINGLY (Uses r16,r17,r18,r20,r22)
CHECK_DIR:
	;ldi		r17, $02		//1 = S, 2 = N, 3 = W, 4 = E
	lds		r22, CURR_DIR
	lds		r17, MOV_DIR
	lds		r18, WPOS
	ldi		ZH, HIGH(SNAKE_FIFO)
	ldi		ZL, LOW(SNAKE_FIFO)
	add		ZL, r18
	ld		r16, Z
	cpi		r17, $04		;JOYSTICK RIGHT
	breq	MOVE_E
	cpi		r17, $03		;JOYSTICK LEFT
	breq	MOVE_W
	cpi		r17, $02		;JOYSTICK NORTH
	breq	MOVE_N
	cpi		r17, $01		;JOYSTICK SOUTH
	breq	MOVE_S
	rjmp	MOVE_DONE
MOVE_E:
	cpi		r22, $03
	breq	MOVE_W
	dec		r16
	ldi		r22, $04
	sts		CURR_DIR, r22
	rjmp	MOVE_DONE
MOVE_W:
	cpi		r22, $04
	breq	MOVE_E
	inc		r16
	ldi		r22, $03
	sts		CURR_DIR, r22
	rjmp	MOVE_DONE
MOVE_N:
	cpi		r22, $01
	breq	MOVE_S
	swap	r16
	inc		r16
	swap	r16
	ldi		r22, $02
	sts		CURR_DIR, r22
	rjmp	MOVE_DONE
MOVE_S:
	cpi		r22, $02
	breq	MOVE_N
	swap	r16
	dec		r16
	swap	r16
	ldi		r22, $01
	sts		CURR_DIR, r22
	rjmp	MOVE_DONE
MOVE_DONE:

	mov		r20, r16
	ret


//IN r20=val ;;;SETS COORD VALUE ON SNAKEHEAD IN SNAKE_FIFO (Uses r16,r17,r20)
FIFO_PUSH:
	lds		r16, RPOS
	lds		r17, SNAKE_LEN
	add		r16, r17
	ldi		ZH, HIGH(SNAKE_FIFO)
	ldi		ZL, LOW(SNAKE_FIFO)
	inc		r16
	andi	r16, 63
	sts		WPOS, r16
	add		ZL,	r16
	st		Z, r20
	ret

//OUT r20=val ;;;READS VALUE FROM SNAKE_FIFO (Uses r16,r20)
FIFO_POP:
	lds		r16, RPOS
	ldi		ZH, HIGH(SNAKE_FIFO)
	ldi		ZL, LOW(SNAKE_FIFO)
	inc		r16					
	andi	r16, 63
	sts		RPOS, r16
	lds		r16, WPOS
	add		ZL, r16
	ld		r20, Z
	ret

CHECK_HIT:
	;cli
	clr		r21
	ldi		YH, HIGH(FOOD)
	ldi		YL, LOW(FOOD)
	add		YL, r16
	ld		r17, Y
	ldi		ZH, HIGH(SNAKE)
	ldi		ZL, LOW(SNAKE)
	add		ZL, r16
	ld		r16, Z
	and		r16, r17
	breq	NO_HIT
HIT:
	lds		r16, RPOS
	dec		r16
	sts		RPOS, r16
	lds		r22, SNAKE_LEN
	inc		r22
	sts		SNAKE_LEN, r22
	st		Y, r2
	call	UPDATE_FOOD
	rjmp	HIT_DONE
NO_HIT:
	call	CLEAR_PIX
	call	SET_PIX
	call	ERASE_SNAKE
HIT_DONE:
	;sei
	ret


UPDATE_FOOD:
	;push	r20
    lds     r20, RANDOMIZER
    andi	r20, 0b01110111
    call	SET_PIX
    ldi     ZH, HIGH(FOOD)
    ldi     ZL, LOW(FOOD)
	add		ZL, r16
	st		Z, r19
	ret

//TRANSLATES FROM SNAKE_FIFO TO VALID COORDS IN VMEM FORMAT (Uses r16,r19,r20)
SET_PIX: 
	ldi		r19, $01
	ldi		r16, $0F
	and		r16, r20
	call	X_LOOP
	ldi		r16, $F0
	and		r16, r20
	call	Y_LOOP
	ret
X_LOOP:
	cpi		r16, 0
	breq	SET_DONE
	cpi		r16, 8
	brsh	COLD
	lsl		r19			;X_VAL
	dec		r16
	rjmp	X_LOOP
Y_LOOP:
	swap	r16			;Y_VAL
	cpi		r16, 8
	brsh	COLD
SET_DONE:
	ret

//TAKES VALUE FROM SNAKE_FIFO AND STORES IT TO SNAKE (Uses r16,r19)
UPDATE_SNAKE: 
	ldi		ZH, HIGH(SNAKE)
	ldi		ZL, LOW(SNAKE)
	add		ZL, r16
	ld		r17, Z
	and		r17, r19
	brne	COLD
	ld		r17, Z
	or		r17, r19
	st		Z, r17
	ret

CLEAR_PIX:
	;CHECK HIT?
	lds		r17, RPOS
	ldi		ZH, HIGH(SNAKE_FIFO)
	ldi		ZL, LOW(SNAKE_FIFO)
	dec		r17 ;RPOS-1
	andi	r17, 63
	add		ZL, r17
	ld		r20, Z ;r20 -> setpix
	ret

//REMOVES THE TAIL IN SNAKE (Uses r16,r19)	
ERASE_SNAKE: 
	ldi		ZH, HIGH(SNAKE)
	ldi		ZL, LOW(SNAKE)
	add		ZL, r16			;Y-val
	ld		r16, Z
	cpi		r16, $0
	breq	ERASE_DONE
	sub		r16, r19		;r19 = X-val
ERASE_DONE:
	st		Z, r16
	ret