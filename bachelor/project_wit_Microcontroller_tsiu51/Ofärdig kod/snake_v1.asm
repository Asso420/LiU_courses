
.equ    SS = PB2
.equ    DD_SCK = PB5
.equ	DD_MOSI = PB3
.equ	PORT_SPI = PORTB
.equ	POSX = 2
.equ	POSY = $FE




INIT:
    ldi        r16, HIGH(RAMEND)
    out        SPH, r16
    ldi        r16, LOW(RAMEND)
    out        SPL, r16
	ldi		r20, 1
 

SPI_MasterInit:
; Set MOSI and SCK output, all others input
	
    ldi        r17,(1<<DD_MOSI)|(1<<DD_SCK)|(1<<SS)
    out        DDRB,r17
; Enable SPI, Master, set clock rate fck/16
    ldi        r17,(1<<SPE)|(1<<MSTR)|(1<<SPR0)
    out        SPCR,r17
   
MAIN:

	call	SPI
	call	SPI_EMPTY
	call	SPI_EMPTY
	call	SPI_EMPTY
	//call	SPI_EMPTY
	//call	WAIT
	//inc		r20
	rjmp	MAIN
SPI:
	cbi		PORT_SPI, SS
	ldi		r16, $00
	call	SPI_MasterTransmit
	ldi		r16, $00
	call	SPI_MasterTransmit
	//ldi		r16, $01

	mov		r16, r20 //TEST
	call	SPI_MasterTransmit
	ldi		r16, $FE
	call	SPI_MasterTransmit
	sbi		PORT_SPI,SS
	ret

SPI_EMPTY:
	cbi		PORT_SPI, SS
	ldi		r16, $00
	call	SPI_MasterTransmit
	ldi		r16, $00
	call	SPI_MasterTransmit
	ldi		r16, $00
	mov		r16, r20		//TEST
	call	SPI_MasterTransmit
	ldi		r16, $FF
	call	SPI_MasterTransmit
	sbi		PORT_SPI,SS
	ret

SPI_MasterTransmit:
; Start transmission of data (r16)
    out        SPDR,r16
Wait_Transmit:
; Wait for transmission complete
    in        r16, SPSR
    sbrs	 r16, SPIF
    rjmp    Wait_Transmit
    ret

WAIT:
	ldi		r22, $FF
OUTER_LOOP:
	ldi		r23, $0F
INNER_LOOP:
	dec		r23
	brne	INNER_LOOP
	dec		r22
	brne	OUTER_LOOP
	ret



END:
	rjmp END

