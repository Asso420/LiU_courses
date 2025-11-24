JOYSTICK: 
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
	reti

CHANNEL:
Y_LED:
	lds     r16,ADMUX
	andi	r16,$fc
	ori		r16,$03 
	rcall	CONVERT
X_LED:
	lds     r16,ADMUX
	andi	r16,$fc
	ori		r16,$02
	rcall	CONVERT      ; (r16=ADMUX value) -> r16=ADCH
	;sts	POSY,r20
EXIT_JOY:
	ret


CONVERT:
	sts		ADMUX,r16
	lds		r16, ADCSRA 
	ori		r16,(1<<ADSC) 
	sts		ADCSRA,r16
	;sbi		ADCSRA, ADSC		; starta en omvandling    
WAIT:
	lds 	r16,ADCSRA
	sbrc	r16,ADSC
	;sbic	ADCSRA,ADSC       ; om nollstlld r vi klara
	rjmp	WAIT              ; annars testa busy-biten igen
	lds		r16, ADCH
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
