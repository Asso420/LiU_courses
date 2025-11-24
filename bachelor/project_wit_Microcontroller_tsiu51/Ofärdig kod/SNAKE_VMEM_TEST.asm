
.equ    SS = PB2
.equ    DD_SCK = PB5
.equ	DD_MOSI = PB3
.equ	PORT_SPI = PORTB
.equ	VMEM_SZ    = 9	
.equ	START_POSX = $80
.equ	START_POSY = $FE
.equ	START_DISP = 0

.dseg
.org	SRAM_START
POSX0:	.byte	1		; Own position
POSY0:	.byte 	1
POSX1:	.byte	1		; Own position
POSY1:	.byte 	1
POSX2:	.byte	1		; Own position
POSY2:	.byte 	1
POSX3:	.byte	1		; Own position
POSY3:	.byte 	1
DISP:	.byte	1
VMEM:	.byte	VMEM_SZ
//TPOSX:	.byte	1		; Target position
//TPOSY:	.byte	1

.cseg
.org	$0


INIT:
    ldi     r16, HIGH(RAMEND)
    out     SPH, r16
    ldi     r16, LOW(RAMEND)
    out     SPL, r16

	ldi		r20, START_POSY
	sts		POSY0, r20
	ldi		r20, START_POSX
	sts		POSX0, r20
	ldi		r20, START_DISP
	sts		DISP, r20
	clr		r20
	sts		POSX1, r20
	sts		POSY1, r20
	sts		POSX2, r20
	sts		POSY2, r20
	sts		POSX3, r20
	sts		POSY3, r20

	ldi		ZH, HIGH(TAB*2)
	ldi		ZL, LOW(TAB*2)
	
	call	ERASE_VMEM

SPI_MasterInit:
; Set MOSI and SCK output, all others input
	
    ldi     r17, (1<<DD_MOSI)|(1<<DD_SCK)|(1<<SS)
    out     DDRB, r17
; Enable SPI, Master, set clock rate fck/16
    ldi     r17, (1<<SPE)|(1<<MSTR)|(0<<SPR0)|(0<<SPR1)
    out     SPCR, r17
   
MAIN:
	//call	ERASE_VMEM
	//call	CMP_POS
	call	DISPLAY_HANDLER
	//ror		r20
	rjmp	MAIN

CHECK_POS1: 
	ldi		r16, $80
	sts		POSX1, r16
	ldi		r16, $FE
	sts		POSY1, r16
	ldi		r16, 1
	sts		DISP, r16
	ret
CHECK_POS0: 
	ldi		r16, $80
	sts		POSX0, r16
	ldi		r16, $FE
	sts		POSY0, r16
	ldi		r16, 0
	sts		DISP, r16
	ret
DISPLAY_HANDLER:
	lds		r24, DISP
/*	cpi		r24, 3
	breq	DISPLAY3
	cpi		r24, 2
	breq	DISPLAY2*/
	cpi		r24, 1
	breq	DISPLAY1
	cpi		r24, 0
	breq	DISPLAY0
	//cp		Z, r20

	ret

DISPLAY0:
	lds		r17, POSX0
	lds		r18, POSY0
	//call	CHECK_POS
	call	SPI_EMPTY
	call	SPI_EMPTY
	call	SPI_EMPTY
	call	SPI
	sbi		PORT_SPI, SS
	call	DELAY
	lds		r17, POSX0
	//clr		r16
	sbrc	r17, 0
 	call	CHECK_POS1
	//sts		DISP, r16
	ror		r17
	sts		POSX0, r17
	ret
DISPLAY1:
	lds		r17, POSX1
	lds		r18, POSY1
	//call	CHECK_POS
	call	SPI_EMPTY
	call	SPI_EMPTY
	call	SPI
	call	SPI_EMPTY
	sbi		PORT_SPI, SS
	call	DELAY
	lds		r17, POSX1
	//clr		r16
	sbrc	r17, 0
 	call	CHECK_POS0
	//sts		DISP, r16
	ror		r17
	sts		POSX1, r17
	ret
DISPLAY2:
	lds		r17, POSX2
	lds		r18, POSY2
	call	SPI_EMPTY
	call	SPI
	call	SPI_EMPTY
	call	SPI_EMPTY
	sbi		PORT_SPI, SS
	call	DELAY
	ret
DISPLAY3:
	lds		r17, POSX3
	lds		r18, POSY3
	call	SPI
	call	SPI_EMPTY
	call	SPI_EMPTY
	call	SPI_EMPTY
	sbi		PORT_SPI, SS
	call	DELAY
	ret
SPI:
	cbi		PORT_SPI, SS
	ldi		r16, $00
	call	SPI_MasterTransmit
	ldi		r16, $00
	call	SPI_MasterTransmit
	mov		r16, r17
	call	SPI_MasterTransmit
	mov		r16, r18
	call	SPI_MasterTransmit
	ret

SPI_EMPTY:
	cbi		PORT_SPI, SS
	ldi		r16, $00
	call	SPI_MasterTransmit
	ldi		r16, $00
	call	SPI_MasterTransmit
	ldi		r16, $00
			//TEST
	call	SPI_MasterTransmit
	ldi		r16, $FF
	call	SPI_MasterTransmit
	ret

SPI_MasterTransmit:
; Start transmission of data (r16)
    out     SPDR, r16
Wait_Transmit:
; Wait for transmission complete
    in      r16, SPSR
    sbrs	r16, SPIF
    rjmp    Wait_Transmit
    ret


/*
RESET_POINT:
	ldi		ZH, HIGH(TAB*2)
	ldi		ZL, LOW(TAB*2)
	ldi		r24, 3
	ret*/
DELAY:
	call	WAIT
	call	WAIT
	call	WAIT
	call	WAIT
	call	WAIT
	call	WAIT
	call	WAIT
	call	WAIT
	call	WAIT
	call	WAIT
	call	WAIT
	call	WAIT
	ret

WAIT:
	ldi		r22, $FF

OUTER_LOOP:
	ldi		r23, $FF
INNER_LOOP:
	dec		r23
	brne	INNER_LOOP
	dec		r22
	brne	OUTER_LOOP
	ret

ERASE_VMEM:
	
/**** 	Radera videominnet						****/
	ldi		ZH, HIGH(VMEM)
	ldi		ZL, LOW(VMEM)
	ldi		r18, 0
	ldi		r16, VMEM_SZ
LOOP_VMEM:
	st		Z+, r18
	dec		r16
	cpi		r16, 0
	brne	LOOP_VMEM
	ret



END:
	rjmp	END

