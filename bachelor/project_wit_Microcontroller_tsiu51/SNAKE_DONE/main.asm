.equ    SS = PB2
.equ    DD_SCK = PB5
.equ	DD_MOSI = PB3
.equ	PORT_SPI = PORTB
.equ	DD_OC1A = PB1
.equ	JOY_STYCK_X = PC3
.equ	JOY_STYCK_Y = PC2
.equ	START_BUTTON = PD1
/*.equ	ADDR_RIGHT8 = $25							
.equ	SLA_W		= (ADDR_RIGHT8 << 1) | 0
.equ	SLA_R		= (ADDR_RIGHT8 << 1) | 1	*/

.equ	SCL = PC5
.equ	SDA = PC4
.def	ZERO_REG = r2

.dseg
.org		0x200
SNAKE:		.byte	8
VMEM_B:		.byte	8
VMEM_G:		.byte	8
VMEM_R:		.byte	8
FOOD:		.byte	8
RAD_INDEX:	.byte	1
CURR_DIR:	.byte	1
MOV_DIR:	.byte   1        //1 = S, 2 = N, 3 = W, 4 = E
MENU_SCR:	.byte	8
RANDOMIZER: .byte	1

.org		0x300
SNAKE_FIFO:	.byte	64
RPOS:		.byte	1
WPOS:		.byte	1
SNAKE_LEN:  .byte	1

.cseg
	.org	0x0000
	rjmp	COLD

	.org	OVF2addr
	jmp		JOYSTICK

	.org	OVF1addr
	jmp		MOVE_MAIN

	.org	OVF0addr
	jmp		MUX

.include "HW_INIT.asm"		;call HW_INIT (USES r16)
.include "START_SCREEN.asm" ;call MENU (USES r16)
.include "MUX.asm"			;call MUX (USES r16, r17, Z)
.include "JOYSTICK.asm"	;call Joystick
.include "MOVE_FIFO.asm"

COLD:
	cli
	clr		r2
	ldi		r16, $2
	sts		MOV_DIR, r16
	sts		CURR_DIR, r16
    ldi     r16, HIGH(RAMEND)
    out     SPH, r16
    ldi     r16, LOW(RAMEND)
    out     SPL, r16
	call	ERASE
	call	HW_INIT
	call	MENU
	call	UPDATE_FOOD

	call	TEST_INSERT ; test
	call	FIFO_INIT

	rjmp		MAIN
   
MAIN:
	;call	JOYSTICK
	;call	MOVE_MAIN
	;call	MUX	
	;call	MOVE_MAIN
	//call	GROW

	rjmp	MAIN

TEST_INSERT:
	ldi		r16, 0b00000011
	sts		SNAKE_FIFO, r16
	ldi		r16, 0b00010011
	sts		SNAKE_FIFO+1, r16
	ldi		r16, 0b00001000
	sts		SNAKE, r16
	ldi		r16, 0b00001000
	sts		SNAKE+1, r16
	ldi		r16, 1
	sts		WPOS, r16
	ldi		r16, 0
	sts		RPOS, r16
	ldi		r16, 1
	sts		SNAKE_LEN, r16
	ret

ERASE:
	ldi		ZH, HIGH(SNAKE)
	ldi		ZL, LOW(SNAKE)
	ldi		r16, 41 ;BYTES TO CLEAR
	call	ERASE_MEM
	ldi		ZH, HIGH(SNAKE_FIFO)
	ldi		ZL, LOW(SNAKE_FIFO)
	ldi		r16, 68 ;BYTES TO CLEAR
	call	ERASE_MEM
	/*ldi		ZH, HIGH(VMEM_B)
	ldi		ZL, LOW(VMEM_B)
	call	ERASE_VMEM
	ldi		ZH, HIGH(VMEM_G)
	ldi		ZL, LOW(VMEM_G)
	call	ERASE_VMEM
	ldi		ZH, HIGH(VMEM_R)
	ldi		ZL, LOW(VMEM_R)
	call	ERASE_VMEM
	ldi		ZH, HIGH(SNAKE)
	ldi		ZL, LOW(SNAKE)
	call	ERASE_VMEM
	ldi		ZH, HIGH(FOOD)
	ldi		ZL, LOW(FOOD)
	call	ERASE_VMEM
	ldi		ZH, HIGH(SNAKE_FIFO)
	ldi		ZL, LOW(SNAKE_FIFO)
	call	ERASE_FIFO*/
	ret

;TEST ERASE SNAKE 1 BYTe
ERASE_FIFO:
	ldi		r18, 0
	ldi		r16, 68
LOOP_VMEM64b:
	st		Z+, r18
	dec		r16
	cpi		r16, 0
	brne	LOOP_VMEM64b
	ret

ERASE_VMEM: ;TEST IN r16 = bytes to clear
	ldi		r18, 0
	ldi		r16, 8
LOOP_VMEM:
	st		Z+, r18
	dec		r16
	cpi		r16, 0
	brne	LOOP_VMEM
	ret

ERASE_MEM: ;TEST IN r16 = bytes to clear
	ldi		r18, 0
	;ldi		r16, 8
LOOP_MEM:
	st		Z+, r18
	dec		r16
	cpi		r16, 0
	brne	LOOP_MEM
	ret

ERASE_VMEM1b:
	ldi		r18, 0
	ldi		r16, 1
LOOP_VMEM1b:
	st		Z+, r18
	dec		r16
	cpi		r16, 0
	brne	LOOP_VMEM1b
	ret

DELAY:					; Delay loop
	push	r19
	push	r20
	push	r21
	ldi		r19, $10
OUTER_DELAY:
	ldi		r20, $FF
MIDDLE_DELAY:
	ldi		r21, $FF
INNER_DELAY:
	dec		r21
	;brne	INNER_DELAY
	dec		r20
	brne	MIDDLE_DELAY
	dec		r19
	brne	OUTER_DELAY
	pop		r21
	pop		r20
	pop		r19
	ret


END:
	jmp	END


RAD:
	;.db		$FE, $FD, $FB, $F7, $EF, $DF, $BF, $7F			//Upp till ner
	.db		$7F, $BF, $DF, $EF, $F7, $FB, $FD, $FE				//Ner till upp
