
.equ    SS = PB2
.equ    DD_SCK = PB5
.equ	DD_MOSI = PB3
.equ	PORT_SPI = PORTB
.equ	VMEM_SZ    = 16	

.dseg
.org	SRAM_START

VMEM:	.byte	VMEM_SZ

.cseg
.org	$0


INIT:
    ldi     r16, HIGH(RAMEND)
    out     SPH, r16
    ldi     r16, LOW(RAMEND)
    out     SPL, r16
	call	ERASE_VMEM

	ldi		r16, $80
	sts		VMEM+14, r16
	ldi		r16, $7f
	sts		VMEM+15, r16
	//HÅRDKODAT ALLT SKA LYSA
	/*ldi		r16, $FF
	sts		VMEM+2, r16		
	sts		VMEM+6, r16
	sts		VMEM+10, r16
	sts		VMEM+10, r16
	clr		r16
	sts		VMEM+3, r16
	sts		VMEM+7, r16
	sts		VMEM+11, r16
	sts		VMEM+15, r16*/
	//sts		VMEM+15, r16


SPI_MasterInit:
; Set MOSI and SCK output, all others input
	
    ldi     r17, (1<<DD_MOSI)|(1<<DD_SCK)|(1<<SS)
    out     DDRB, r17
; Enable SPI, Master, set clock rate fck/16
    ldi     r17, (1<<SPE)|(1<<MSTR)|(0<<SPR0)|(0<<SPR1)
    out     SPCR, r17
   
MAIN:
	call	RST_VMEM_PTR 
	call	DISPLAY
	rjmp	MAIN



;RESETS POINTER TO BEGGINING OF VMEM
RST_VMEM_PTR:
	ldi		r21, 4
	ldi		XH, HIGH(VMEM) 
	ldi		XL, LOW(VMEM)
	ret

; 
DISPLAY:
	call	LOAD_PTR
	call	SPI
	dec		r21
	brne	DISPLAY
	sbi		PORT_SPI, SS
	call	DELAY
	ret

;POINTER TO NEXT BYTE AND LOAD
LOAD_PTR:
	ld		r17, X+
	ld		r18, X+
	ld		r19, X+
	ld		r20, X+
	ret
SPI:
	cbi		PORT_SPI, SS
	mov		r16, r17
	call	SPI_MasterTransmit
	mov		r16, r18
	call	SPI_MasterTransmit
	mov		r16, r19
	call	SPI_MasterTransmit
	mov		r16, r20
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

