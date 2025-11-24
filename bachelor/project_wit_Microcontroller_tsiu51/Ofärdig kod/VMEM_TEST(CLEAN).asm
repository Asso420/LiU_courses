
.equ    SS = PB2
.equ    DD_SCK = PB5
.equ	DD_MOSI = PB3
.equ	PORT_SPI = PORTB
.def	ZERO_REG = r2

.dseg
.org		0x200
VMEM_B:		.byte	8
VMEM_G:		.byte	8
VMEM_R:		.byte	8
RAD_INDEX:	.byte	1


.cseg

	.org	0x00
	rjmp	COLD

	.org	0x0020
	jmp		MUX


COLD:
    ldi     r16, HIGH(RAMEND)
    out     SPH, r16
    ldi     r16, LOW(RAMEND)
    out     SPL, r16
	call	HW_INIT
	call	ERASE_VMEM
	jmp		MAIN

HW_INIT:
; Set MOSI and SCK output, all others input
    ldi     r16, (1<<DD_MOSI)|(1<<DD_SCK)|(1<<SS)
    out     DDRB, r16

; Enable SPI, Master, set clock rate fck/16
    ldi     r16, (1<<SPE)|(1<<MSTR)|(0<<SPR0)|(0<<SPR1)
    out     SPCR, r16
	cbi		PORT_SPI, SS

	ldi		r16, (1<<CS02);|(0<<CS01)|(0<<CS00) // Prescale 256
	out		TCCR0B, r16
	ldi		r16,(1<<TOIE0)
	sts		TIMSK0, r16


	sei
	
	ret


   
MAIN:
	call	TEST_INSERT
	;call	XD
	call	MUX
	;call	DELAY
	rjmp	MAIN

TEST_INSERT:
	ldi		r16,$01
	sts		VMEM_B,r16
	ldi		r16,$02
	sts		VMEM_G+1,r16
	ldi		r16,$04
	sts		VMEM_R+2,r16
	ret

MUX:
	push	ZH
	push	ZL
	push	r16
	push	r17

	lds		r17,RAD_INDEX
	ldi		ZH,HIGH(VMEM_B)
	ldi		ZL,LOW(VMEM_B)
	add		ZL,r17
	;adc		ZH,ZERO_REG
	ld		r16,Z
	call	SPI

	ldi		ZH,HIGH(VMEM_G)
	ldi		ZL,LOW(VMEM_G)
	add		ZL,r17
	;adc		ZH,ZERO_REG
	ld		r16,Z
	call	SPI

	ldi		ZH,HIGH(VMEM_R)
	ldi		ZL,LOW(VMEM_R)
	add		ZL,r17
	;adc		ZH,ZERO_REG
	ld		r16,Z
	call	SPIzzzzzz

	ldi		ZH,HIGH(RAD*2)
	ldi		ZL,LOW(RAD*2)
	add		ZL,r17
	;adc		ZH,ZERO_REG
	lpm		r16,Z
	call	SPI

	jmp		SEND
SPI:
	out     SPDR, r16
	call	Wait_Transmit
	ret
SEND:
	sbi		PORT_SPI, SS
	cbi		PORT_SPI, SS

	inc		r17				
	sbrc	r17,4
	clr		r17
	sts		RAD_INDEX,r17			//inc RAD_INDEX, unless RAD_INDEX>7
MUX_DONE:
	pop		r17
	pop		ZL
	pop		ZH
	pop		r16
	out		SREG,r16
	pop		r16
	retizzzzzzzzMasterTransmit:
; Start transmission of data (r16)
    out     SPDR, r16
Wait_Transmit:
; Wait for transmission complete
    in      r16, SPSR
    sbrs	r16, SPIF
    rjmp    Wait_Transmit
    ret

DELAY:
	call	WAIT
	ret

WAIT:
	ldi		r21, $FF
OUTER_LOOP2:
	ldi		r22, $FF
OUTER_LOOP:
	ldi		r23, $FF
INNER_LOOP:
	dec		r23
	brne	INNER_LOOP
	dec		r22
	brne	OUTER_LOOP
	dec		r21
	brne	OUTER_LOOP2
	ret

ERASE_VMEM:
	ldi		r18, 0
	ldi		r16, 8
	call	GREEN
	call	BLUE
	call	RED
	ret
GREEN:								//Erase Green
	ldi		ZH, HIGH(VMEM_G)
	ldi		ZL, LOW(VMEM_G)
	jmp		LOOP_VMEM
BLUE:								//Erase Blue
	ldi		r16,8
	ldi		ZH, HIGH(VMEM_B)
	ldi		ZL, LOW(VMEM_B)
	jmp		LOOP_VMEM
RED:								//Erase Red
	ldi		r16,8
	ldi		ZH, HIGH(VMEM_R)
	ldi		ZL, LOW(VMEM_R)
	jmp		LOOP_VMEM
LOOP_VMEM:							//Erase
	st		Z+, r18
	dec		r16
	cpi		r16, 0
	brne	LOOP_VMEM
	ret



RAD:
	;.db		$FE, $FD, $FB, $F7, $EF, $DF, $BF, $7F			//Upp till ner
	.db		$7F, $BF, $DF, $EF, $F7, $FB, $FD, $FE				//Ner till upp
