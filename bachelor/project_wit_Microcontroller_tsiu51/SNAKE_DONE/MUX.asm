MUX:
	push	ZH
	push	ZL
	push	r17
	push	r16
	in		r16, SREG
	push	r16
	push	r18
	//call	ERASE_VMEM
	lds		r18, RANDOMIZER
	inc		r18
	sts		RANDOMIZER, r18
	ldi		ZH, HIGH(VMEM_B)
	ldi		ZL, LOW(VMEM_B)
	ldi		r16, 16
	call	ERASE_MEM
/*	ldi		ZH, HIGH(VMEM_B)
	ldi		ZL, LOW(VMEM_B)
	call	ERASE_VMEM
	ldi		ZH, HIGH(VMEM_G)
	ldi		ZL, LOW(VMEM_G)
	call	ERASE_VMEM
	ldi		ZH, HIGH(VMEM_R)
	ldi		ZL, LOW(VMEM_R)
	CALL	ERASE_VMEM*/

	call	UPDATE_COORD
	;call	MENU
MUXEN:
	lds		r17, RAD_INDEX
	ldi		ZH, HIGH(VMEM_B)
	ldi		ZL, LOW(VMEM_B)
	add		ZL, r17
	ld		r16, Z
	call	SPI

	ldi		ZH, HIGH(VMEM_G)
	ldi		ZL, LOW(VMEM_G)
	add		ZL, r17
	ld		r16, Z
	call	SPI

	ldi		ZH, HIGH(VMEM_R)
	ldi		ZL, LOW(VMEM_R)
	add		ZL, r17
	ld		r16, Z
	call	SPI

	ldi		ZH, HIGH(RAD*2)
	ldi		ZL, LOW(RAD*2)
	add		ZL, r17
	lpm		r16, Z
	call	SPI

	jmp		SEND
SPI:
	out     SPDR, r16
	call	Wait_Transmit
	ret
SEND:
	sbi		PORT_SPI, SS
	;cbi		PORT_SPI, SS

	inc		r17				
	sbrc	r17, 3
	clr		r17
	sts		RAD_INDEX, r17			//inc RAD_INDEX, unless RAD_INDEX>7
MUX_DONE:
	pop		r18
	pop		r16
	out		SREG, r16
	pop		r16
	pop		r17
	pop		ZL
	pop		ZH
	cbi		PORT_SPI, SS
	reti  ;;;;;;;;;;;;;RETI
	
SPI_MasterTransmit:
; Start transmission of data (r16)
    out     SPDR, r16
Wait_Transmit:
; Wait for transmission complete
    in      r16, SPSR
    sbrs	r16, SPIF
    rjmp    Wait_Transmit
    ret

UPDATE_COORD:
	lds		r16, SNAKE
	sts		VMEM_B, r16
	lds		r16, SNAKE+1
	sts		VMEM_B+1, r16
	lds		r16, SNAKE+2
	sts		VMEM_B+2, r16
	lds		r16, SNAKE+3
	sts		VMEM_B+3, r16
	lds		r16, SNAKE+4
	sts		VMEM_B+4, r16
	lds		r16, SNAKE+5
	sts		VMEM_B+5, r16
	lds		r16, SNAKE+6
	sts		VMEM_B+6, r16
	lds		r16, SNAKE+7
	sts		VMEM_B+7, r16
	//ret
	lds		r16, FOOD
	sts		VMEM_G, r16
	lds		r16, FOOD+1
	sts		VMEM_G+1, r16
	lds		r16, FOOD+2
	sts		VMEM_G+2, r16
	lds		r16, FOOD+3
	sts		VMEM_G+3, r16
	lds		r16, FOOD+4
	sts		VMEM_G+4, r16
	lds		r16, FOOD+5
	sts		VMEM_G+5, r16
	lds		r16, FOOD+6
	sts		VMEM_G+6, r16
	lds		r16, FOOD+7
	sts		VMEM_G+7, r16	

	
	lds		r16, MENU_SCR
	sts		VMEM_R, r16
	lds		r16, MENU_SCR+1
	sts		VMEM_R+1, r16
	lds		r16, MENU_SCR+2
	sts		VMEM_R+2, r16
	lds		r16, MENU_SCR+3
	sts		VMEM_R+3, r16
	lds		r16, MENU_SCR+4
	sts		VMEM_R+4, r16
	lds		r16, MENU_SCR+5
	sts		VMEM_R+5, r16
	lds		r16, MENU_SCR+6
	sts		VMEM_R+6, r16
	lds		r16, MENU_SCR+7
	sts		VMEM_R+7, r16

	ret
