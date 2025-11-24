
.equ    SS = PB2
.equ    DD_SCK = PB5
.equ	DD_MOSI = PB3
.equ	PORT_SPI = PORTB

    ldi        r16, HIGH(RAMEND)
    out        SPH, r16
    ldi        r16, LOW(RAMEND)
    out        SPL, r16

//INIT:


 

SPI_MasterInit:
; Set MOSI and SCK output, all others input
	
    ldi        r17,(1<<DD_MOSI)|(1<<DD_SCK)|(1<<SS)
    out        DDRB,r17
; Enable SPI, Master, set clock rate fck/16
    ldi        r17,(1<<SPE)|(1<<MSTR)|(1<<SPR0)
    out        SPCR,r17
   

MAIN:
	cbi		PORT_SPI, SS
	ldi		r16,$01
	call	SPI_MasterTransmit
	ldi		r16,$01
	call	SPI_MasterTransmit
	ldi		r16,$01
	call	SPI_MasterTransmit
	ldi		r16,$fe
	call	SPI_MasterTransmit
	sbi		PORT_SPI,SS
	rjmp	MAIN
SPI_MasterTransmit:
; Start transmission of data (r16)
    out        SPDR,r16
Wait_Transmit:
; Wait for transmission complete
    in        r16, SPSR
    sbrs	 r16, SPIF
    rjmp    Wait_Transmit
    ret

/*SPI_MasterTransmit2:
	ldi		r17,$40
    out        SPDR,r17
Wait_Transmit2:
    in        r16, SPSR
    sbrs	 r16, SPIF
    rjmp    Wait_Transmit2
    ;ret
	
SPI_MasterTransmit3:
	ldi		r17,$40
    out        SPDR,r17
Wait_Transmit3:
    in        r16, SPSR
    sbrs	 r16, SPIF
    rjmp    Wait_Transmit3
    ;ret
	
		SPI_MasterTransmit4:
	ldi		r17,$40
    out        SPDR,r17
Wait_Transmit4:
    in        r16, SPSR
    sbrs	 r16, SPIF
    rjmp    Wait_Transmit4
    
;ret*/
	
