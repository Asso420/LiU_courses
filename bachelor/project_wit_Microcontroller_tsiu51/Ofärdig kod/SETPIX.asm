SETPIX:
	//call	FIFO_PUSH
	// KOLLA OM TRÄFF PÅ MAT //
	//call	FIFO_POP    // OM INGEN TRÄFF
	//ldi		r20, FIF0_POP  //FIFO_POP VALUE
	ldi		r19, $01
	ldi		r18, $01
	ldi		r16, $0F
	and		r16, r20
	call	X_LOOP
	ldi		r16, $F0
	and		r16, r20
	call	Y_LOOP
	ret
X_LOOP:
	lsl		r19
	dec		r16
	breq	SET_DONE
	rjmp	X_LOOP
Y_LOOP:
	swap	r16
	lsl		r18
	dec		r16
	breq	SET_DONE
	rjmp	Y_LOOP
SET_DONE:
	ret
