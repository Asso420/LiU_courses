JOYSTICK: 
	;cli
	push	ZH
	push	ZL
	push	r18
	push	r17
	push	r16
	clr		r17
	rcall	CHANNEL
	pop		r16
	pop		r17
	pop		r18
	pop		ZL
	pop		ZH
	;sei
	reti  ;;;;;;;;;;;;RETI

CHANNEL:
	clr		r15
Y_LED:
	lds     r16,ADMUX
	andi	r16,$fc
	ori		r16,$03 
	rcall	CONVERT
	;sts		VMEM_R+7, r17
X_LED:
	lds     r16,ADMUX
	andi	r16,$fc
	ori		r16,$02
	rcall	CONVERT      ; (r16=ADMUX value) -> r16=ADCH
	;sts		VMEM_R+6, r17
	;sts	POSY,r20
	;sts		VMEM_R+5, r15
EXIT_JOY:
	ret


CONVERT:
/*	ori		r16, (1<<ADLAR)  ; test to use 8-bit results*/
	sts		ADMUX,r16
	lds		r16, ADCSRA 
	ori		r16,(1<<ADSC) 
	sts		ADCSRA,r16
	; starta en omvandling    
WAIT:
	lds 	r16,ADCSRA
	sbrc	r16,ADSC
	rjmp	WAIT              ; annars testa busy-biten igen
	lds		r16, ADCH

/*	swap	r16
	andi	r16, 0x0f*/

	; test
/*	swap	r15
	or	r15, r16*/


	inc		r17
	cpi		r16,$00
	breq	STORE
	inc		r17
	cpi		r16,$03
	breq	STORE
	ret
STORE:
	sts		MOV_DIR,r17         ; En lsning av hg byte
	ret
