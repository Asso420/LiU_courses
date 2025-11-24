HW_INIT:
; Set MOSI and SCK output, all others input
    ldi     r16, (1<<DD_MOSI)|(1<<DD_SCK)|(1<<SS)|(1<<DD_OC1A)
    out     DDRB, r16

; Enable SPI, Master, set clock rate fck/64
    ldi     r16, (1<<SPE)|(1<<MSTR)|(0<<SPR0)|(1<<SPR1) //DISPLAY
    out     SPCR, r16
	cbi		PORT_SPI, SS

	ldi		r16, (0<<CS02)|(0<<CS01)|(1<<CS00) // Prescale 64 / MUX interrupt
	out		TCCR0B, r16
	ldi		r16, (1<<TOIE0)
	sts		TIMSK0, r16

	ldi		r16, (0<<CS22)|(1<<CS21)|(1<<CS20) //JOYSTICK interrupt
	sts		TCCR2B, r16
	ldi		r16, (1<<TOIE2) 
	sts		TIMSK2, r16

;AD_INIT: 
	ldi		r16, (1<<REFS0) | (0<<REFS1) | (0<<ADLAR) ;| (1<<MUX3) | (1<<MUX2) | (1<<MUX1) | (1<<MUX0)
	sts		ADMUX,r16
	ldi		r16, (1<<ADEN) | (0<<ADSC) | (1<<ADPS2) | (1<<ADPS1) | (1<<ADPS0) 
	sts		ADCSRA,r16


	ldi		r16, (0<<TOIE1) //DISABLE
	sts		TIMSK1, r16


	sei

	ret

FIFO_INIT:
	
	ldi		r16, (0<<CS12)|(1<<CS11)|(1<<CS10) //Movement interrupt
	sts		TCCR1B, r16
	ldi		r16, (1<<TOIE1) //
	sts		TIMSK1, r16
	ret