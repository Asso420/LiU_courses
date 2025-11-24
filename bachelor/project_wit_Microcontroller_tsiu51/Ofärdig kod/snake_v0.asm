
	.equ	SS = PB2
	.equ	DD_MOSI = PB3
	.equ	DD_SCK = PB5
INIT:

	ldi		r16, HIGH(RAMEND)
	out		SPH, r16
	ldi		r16, LOW(RAMEND)
	out		SPL, r16

	sbi		DDRB, SS

SPI_MasterInit:
; Set MOSI and SCK output, all others input
	ldi		r17,(1<<DD_MOSI)|(1<<DD_SCK)
	out		DDRB,r17
; Enable SPI, Master, set clock rate fck/16
	ldi		r17,(1<<SPE)|(1<<MSTR)|(1<<SPR0)
	out		SPCR,r17
	ret
SPI_MasterTransmit:
; Start transmission of data (r16)
	out		SPDR,r16
Wait_Transmit:
; Wait for transmission complete
	in		r16, SPSR
	sbrs	r16, SPIF
	rjmp	Wait_Transmit
	ret



	ldi		r16, 0
	call	SPI_MasterTransmit
	clr		r16
	call	SPI_MasterTransmit
	clr		r16
	call	SPI_MasterTransmit
	clr		r16
	call	SPI_MasterTransmit
	

