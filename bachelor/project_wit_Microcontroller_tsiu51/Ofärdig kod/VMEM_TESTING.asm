.equ    SS = PB2
.equ    DD_SCK = PB5
.equ	DD_MOSI = PB3
.equ	PORT_SPI = PORTB
/*
.equ	Screen_1 = 0
.equ	Screen_2 = 8
.equ	Screen_3 = 16
.equ	Screen_4 = 24
.equ	Rad_0	= 1
.equ	Rad_1	= 2
.equ	Rad_2	= 3
.equ	Rad_3	= 4
.equ	Rad_4	= 5
.equ	Rad_5	= 6
.equ	Rad_6	= 7
.equ	Rad_7	= 8
*/
.def	ZERO_REG = r2

.dseg
.org	0x200
VMEM_B:		.byte	8
VMEM_G:		.byte	8
VMEM_R:		.byte	8
RAD_INDEX:	.byte	1

.cseg

	.org	0x00
	rjmp	INIT

	.org	0x0020
	jmp		MUX_TEST2


INIT:
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

;TIMER0_INIT
	ldi		r16, (1<<CS02);|(0<<CS01)|(0<<CS00) // Prescale 256
	out		TCCR0B, r16
	ldi		r16,(1<<TOIE0)
	sts		TIMSK0, r16
	sei
	
	ret
/*
TIM0_OVF:
	push	r16
	in		r16,SREG
	push	r16
	push	ZH
	push	ZL
	push	r17
	call	MUX_TEST2
	pop		r17
	pop		ZL
	pop		ZH
	pop		r16
	out		SREG,r16
	pop		r16
	reti
*/
   
MAIN:
	call	TEST2
	;call	XD
	;call	MUX_TEST2
	call	DELAY
	rjmp	MAIN

TEST2:
	ldi		r16,$01
	sts		VMEM_B,r16
	ldi		r16,$02
	sts		VMEM_G+1,r16
	ldi		r16,$04
	sts		VMEM_R+2,r16
	ret

MUX_TEST2:
	push	r16
	in		r16,SREG
	push	r16
	push	ZH
	push	ZL
	push	r17
	lds		r17,RAD_INDEX
CONTINUEMUX:
	ldi		ZH,HIGH(VMEM_B)
	ldi		ZL,LOW(VMEM_B)
	add		ZL,r17
	adc		ZH,ZERO_REG
	ld		r16,Z
	cbi		PORT_SPI, SS
	call	SEND

	
	ldi		ZH,HIGH(VMEM_G)
	ldi		ZL,LOW(VMEM_G)
	add		ZL,r17
	adc		ZH,ZERO_REG
	ld		r16,Z
	call	SEND

	ldi		ZH,HIGH(VMEM_R)
	ldi		ZL,LOW(VMEM_R)
	add		ZL,r17
	adc		ZH,ZERO_REG
	ld		r16,Z
	call	SEND

	ldi		ZH,HIGH(RAD*2)
	ldi		ZL,LOW(RAD*2)
	add		ZL,r17
	adc		ZH,ZERO_REG
	lpm		r16,Z
	call	SEND
	sbi		PORT_SPI, SS

	inc		r17
	sts		RAD_INDEX,r17
	cpi		r17,8
	breq	MUX_DONE2
SEND:
	call	SPI_MasterTransmit
	ret
MUX_DONE2:
	pop		r17
	pop		ZL
	pop		ZH
	pop		r16
	out		SREG,r16
	pop		r16
	reti
	

SPI_MasterTransmit:
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
GREEN:
	ldi		ZH, HIGH(VMEM_G)
	ldi		ZL, LOW(VMEM_G)
	jmp		LOOP_VMEM
BLUE:
	ldi		r16,8
	ldi		ZH, HIGH(VMEM_B)
	ldi		ZL, LOW(VMEM_B)
	jmp		LOOP_VMEM
RED:
	ldi		r16,8
	ldi		ZH, HIGH(VMEM_R)
	ldi		ZL, LOW(VMEM_R)
	jmp		LOOP_VMEM
LOOP_VMEM:
	st		Z+, r18
	dec		r16
	cpi		r16, 0
	brne	LOOP_VMEM
	ret


/*
TEST:
	ldi		ZH,HIGH(SNAKE*2)
	ldi		ZL,LOW(SNAKE*2)
	ld		r16,Z+
	sts		VMEM_G+(Screen_1+Rad_1),r16
	ld		r16,Z+
	sts		VMEM_G+(Screen_1+Rad_2),r16
	ld		r16,Z+
	sts		VMEM_G+(Screen_1+Rad_3),r16
	ld		r16,Z+
	sts		VMEM_G+(Screen_1+Rad_4),r16
	ld		r16,Z+
	sts		VMEM_G+(Screen_1+Rad_5),r16
	ld		r16,Z+
	sts		VMEM_G+(Screen_1+Rad_6),r16
	ld		r16,Z+

	sts		VMEM_G+(Screen_2+Rad_1),r16
	ld		r16,Z+
	sts		VMEM_G+(Screen_2+Rad_2),r16
	ld		r16,Z+
	sts		VMEM_G+(Screen_2+Rad_3),r16
	ld		r16,Z+
	sts		VMEM_G+(Screen_2+Rad_4),r16
	ld		r16,Z+
	sts		VMEM_G+(Screen_2+Rad_5),r16
	ld		r16,Z+
	sts		VMEM_G+(Screen_2+Rad_6),r16

	ld		r16,Z+
	sts		VMEM_G+(Screen_3+Rad_2),r16
	ld		r16,Z+
	sts		VMEM_G+(Screen_3+Rad_3),r16
	ld		r16,Z+
	sts		VMEM_G+(Screen_3+Rad_4),r16
	ld		r16,Z+
	sts		VMEM_G+(Screen_3+Rad_5),r16
	ld		r16,Z+
	sts		VMEM_G+(Screen_3+Rad_6),r16
	ld		r16,Z+
	sts		VMEM_G+(Screen_3+Rad_7),r16

	ld		r16,Z+
	sts		VMEM_G+(Screen_4+Rad_2),r16
	ld		r16,Z+
	sts		VMEM_G+(Screen_4+Rad_2),r16
	ld		r16,Z+
	sts		VMEM_G+(Screen_4+Rad_2),r16
	ld		r16,Z+
	sts		VMEM_G+(Screen_4+Rad_2),r16
	ld		r16,Z+
	sts		VMEM_G+(Screen_4+Rad_2),r16
	ld		r16,Z+
	sts		VMEM_G+(Screen_4+Rad_2),r16

MUX_TEST:
	push	ZL
	push	ZH
	push	r17
	push	r19

	lds		r16, Screen_4
	call	SEND
	lds		r16, Screen_3
	call	SEND
	lds		r16, Screen_2
	call	SEND
	lds		r16, Screen_1
	call	SEND
	jmp		MUX_DONE
SEND:
	cbi		PORT_SPI, SS
	mov		r17, RAD_INDEX
	cpi		r17, 8
	breq	MUX_DONE
	ldi		ZH,HIGH(VMEM_B)
	ldi		ZL,LOW(VMEM_B)
	add		r17,r16
	add		ZL,r17 
	adc		ZH,ZERO_REG
	ld		r16,Z
	call	SPI_MasterTransmit

	ldi		ZH,HIGH(VMEM_G)
	ldi		ZL,LOW(VMEM_G)
	add		r17,r16
	add		ZL,r17
	adc		ZH,ZERO_REG
	ld		r16,Z
	call	SPI_MasterTransmit

	ldi		ZH,HIGH(VMEM_R)
	ldi		ZL,LOW(VMEM_R)
	add		r17,r16
	add		ZL,r17
	adc		ZH,ZERO_REG
	ld		r16,Z
	call	SPI_MasterTransmit

	ldi		ZH,HIGH(RAD*2)
	ldi		ZL,LOW(RAD*2)
	add		r17,r16
	add		ZL,r17
	adc		ZH,ZERO_REG
	ld		r16,Z
	call	SPI_MasterTransmit
	sbi		PORT_SPI, SS
	inc		RAD_INDEX
	ret
MUX_DONE:
	pop		r19
	pop		r17
	pop		ZH
	pop		ZL
	ret
*/
END:
	rjmp	END


SNAKE:
	.db		$13, $3B, $6F, $70, $7F, $3F, $C0, $D0, $B8, $74, $F4, $E4, $0F, $0F, $17, $17, $1F ,$0F , $80, $C0, $40 , $60, $E0, $C0

RAD:
	;.db		$FE, $FD, $FB, $F7, $EF, $DF, $BF, $7F
	.db		$7F, $BF, $DF, $EF, $F7, $FB, $FD, $FE



	
