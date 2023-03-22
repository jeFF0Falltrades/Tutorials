	.file	"practice.c"
	.text
	.def	_printf;	.scl	3;	.type	32;	.endef
_printf:
LFB8:
	.cfi_startproc
	pushl	%ebp
	.cfi_def_cfa_offset 8
	.cfi_offset 5, -8
	movl	%esp, %ebp
	.cfi_def_cfa_register 5
	pushl	%ebx
	subl	$36, %esp
	.cfi_offset 3, -12
	leal	12(%ebp), %eax
	movl	%eax, -16(%ebp)
	movl	-16(%ebp), %ebx
	movl	$1, (%esp)
	movl	__imp____acrt_iob_func, %eax
	call	*%eax
	movl	%ebx, 8(%esp)
	movl	8(%ebp), %edx
	movl	%edx, 4(%esp)
	movl	%eax, (%esp)
	call	___mingw_vfprintf
	movl	%eax, -12(%ebp)
	movl	-12(%ebp), %eax
	movl	-4(%ebp), %ebx
	leave
	.cfi_restore 5
	.cfi_restore 3
	.cfi_def_cfa 4, 4
	ret
	.cfi_endproc
LFE8:
	.globl	_global
	.data
	.align 4
_global:
	.long	13
	.section .rdata,"dr"
LC0:
	.ascii "****Running %s()****\12\12\0"
	.text
	.globl	_print_function_header
	.def	_print_function_header;	.scl	2;	.type	32;	.endef
_print_function_header:
LFB38:
	.cfi_startproc
	pushl	%ebp
	.cfi_def_cfa_offset 8
	.cfi_offset 5, -8
	movl	%esp, %ebp
	.cfi_def_cfa_register 5
	subl	$24, %esp
	movl	8(%ebp), %eax
	movl	%eax, 4(%esp)
	movl	$LC0, (%esp)
	call	_printf
	nop
	leave
	.cfi_restore 5
	.cfi_def_cfa 4, 4
	ret
	.cfi_endproc
LFE38:
	.section .rdata,"dr"
LC1:
	.ascii "quick_maths\0"
LC2:
	.ascii "Uh-oh, no memory left!\0"
LC3:
	.ascii "\11%d + %d = %d\12\12\0"
LC4:
	.ascii "\11%d - %d = %d\12\12\0"
LC5:
	.ascii "\11%d * %d = %d\12\12\0"
LC6:
	.ascii "\11%d / %d = %d\12\12\0"
LC7:
	.ascii "\11%d %% %d = %d\12\12\0"
LC8:
	.ascii "\11%d << 2 = %d\12\12\0"
LC9:
	.ascii "\11%d >> 1 = %d\12\12\0"
	.align 4
LC10:
	.ascii "\11Chars can shift too!\12\11%c << 3 = %c\12\12\0"
LC11:
	.ascii "\11%d & 2 = %d\12\12\0"
LC12:
	.ascii "\11%d | 2 = %d\12\12\0"
LC13:
	.ascii "\11%d ^ %d = %d\12\12\0"
LC14:
	.ascii "\11%d + 2 == %d is %d\12\12\0"
LC15:
	.ascii "\11%d == %d is %d\12\12\0"
LC16:
	.ascii "\11%d <= %d is %d\12\12\0"
	.text
	.globl	_quick_maths
	.def	_quick_maths;	.scl	2;	.type	32;	.endef
_quick_maths:
LFB39:
	.cfi_startproc
	pushl	%ebp
	.cfi_def_cfa_offset 8
	.cfi_offset 5, -8
	movl	%esp, %ebp
	.cfi_def_cfa_register 5
	subl	$40, %esp
	movl	$LC1, (%esp)
	call	_print_function_header
	movl	$3, -12(%ebp)
	movl	$4, (%esp)
	call	_malloc
	movl	%eax, -16(%ebp)
	cmpl	$0, -16(%ebp)
	jne	L5
	movl	$LC2, (%esp)
	call	_printf
	movl	$0, %eax
	jmp	L6
L5:
	movl	-16(%ebp), %eax
	movl	$5, (%eax)
	movb	$109, -17(%ebp)
	movl	8(%ebp), %edx
	movl	12(%ebp), %eax
	addl	%edx, %eax
	movl	%eax, 12(%esp)
	movl	12(%ebp), %eax
	movl	%eax, 8(%esp)
	movl	8(%ebp), %eax
	movl	%eax, 4(%esp)
	movl	$LC3, (%esp)
	call	_printf
	movl	8(%ebp), %eax
	subl	12(%ebp), %eax
	movl	%eax, 12(%esp)
	movl	12(%ebp), %eax
	movl	%eax, 8(%esp)
	movl	8(%ebp), %eax
	movl	%eax, 4(%esp)
	movl	$LC4, (%esp)
	call	_printf
	movl	8(%ebp), %eax
	imull	12(%ebp), %eax
	movl	%eax, 12(%esp)
	movl	12(%ebp), %eax
	movl	%eax, 8(%esp)
	movl	8(%ebp), %eax
	movl	%eax, 4(%esp)
	movl	$LC5, (%esp)
	call	_printf
	movl	8(%ebp), %eax
	cltd
	idivl	12(%ebp)
	movl	%eax, 12(%esp)
	movl	12(%ebp), %eax
	movl	%eax, 8(%esp)
	movl	8(%ebp), %eax
	movl	%eax, 4(%esp)
	movl	$LC6, (%esp)
	call	_printf
	movl	8(%ebp), %eax
	cltd
	idivl	12(%ebp)
	movl	%edx, %eax
	movl	%eax, 12(%esp)
	movl	12(%ebp), %eax
	movl	%eax, 8(%esp)
	movl	8(%ebp), %eax
	movl	%eax, 4(%esp)
	movl	$LC7, (%esp)
	call	_printf
	movl	-12(%ebp), %eax
	sall	$2, %eax
	movl	%eax, 8(%esp)
	movl	-12(%ebp), %eax
	movl	%eax, 4(%esp)
	movl	$LC8, (%esp)
	call	_printf
	movl	_global, %eax
	sarl	%eax
	movl	%eax, %edx
	movl	_global, %eax
	movl	%edx, 8(%esp)
	movl	%eax, 4(%esp)
	movl	$LC9, (%esp)
	call	_printf
	movsbl	-17(%ebp), %eax
	leal	0(,%eax,8), %edx
	movsbl	-17(%ebp), %eax
	movl	%edx, 8(%esp)
	movl	%eax, 4(%esp)
	movl	$LC10, (%esp)
	call	_printf
	movl	-16(%ebp), %eax
	movl	(%eax), %eax
	andl	$2, %eax
	movl	%eax, %edx
	movl	-16(%ebp), %eax
	movl	(%eax), %eax
	movl	%edx, 8(%esp)
	movl	%eax, 4(%esp)
	movl	$LC11, (%esp)
	call	_printf
	movl	-16(%ebp), %eax
	movl	(%eax), %eax
	orl	$2, %eax
	movl	%eax, %edx
	movl	-16(%ebp), %eax
	movl	(%eax), %eax
	movl	%edx, 8(%esp)
	movl	%eax, 4(%esp)
	movl	$LC12, (%esp)
	call	_printf
	movl	-16(%ebp), %eax
	movl	(%eax), %eax
	xorl	-12(%ebp), %eax
	movl	%eax, %edx
	movl	-16(%ebp), %eax
	movl	(%eax), %eax
	movl	%edx, 12(%esp)
	movl	%eax, 8(%esp)
	movl	-12(%ebp), %eax
	movl	%eax, 4(%esp)
	movl	$LC13, (%esp)
	call	_printf
	movl	-12(%ebp), %eax
	leal	2(%eax), %edx
	movl	-16(%ebp), %eax
	movl	(%eax), %eax
	cmpl	%eax, %edx
	sete	%al
	movzbl	%al, %edx
	movl	-16(%ebp), %eax
	movl	(%eax), %eax
	movl	%edx, 12(%esp)
	movl	%eax, 8(%esp)
	movl	-12(%ebp), %eax
	movl	%eax, 4(%esp)
	movl	$LC14, (%esp)
	call	_printf
	movl	-16(%ebp), %eax
	movl	(%eax), %eax
	cmpl	%eax, -12(%ebp)
	sete	%al
	movzbl	%al, %edx
	movl	-16(%ebp), %eax
	movl	(%eax), %eax
	movl	%edx, 12(%esp)
	movl	%eax, 8(%esp)
	movl	-12(%ebp), %eax
	movl	%eax, 4(%esp)
	movl	$LC15, (%esp)
	call	_printf
	movl	-16(%ebp), %eax
	movl	(%eax), %eax
	cmpl	%eax, -12(%ebp)
	setle	%al
	movzbl	%al, %edx
	movl	-16(%ebp), %eax
	movl	(%eax), %eax
	movl	%edx, 12(%esp)
	movl	%eax, 8(%esp)
	movl	-12(%ebp), %eax
	movl	%eax, 4(%esp)
	movl	$LC16, (%esp)
	call	_printf
	movl	-16(%ebp), %eax
	movl	%eax, (%esp)
	call	_free
	movl	$0, -16(%ebp)
	movl	12(%ebp), %eax
	subl	8(%ebp), %eax
L6:
	leave
	.cfi_restore 5
	.cfi_def_cfa 4, 4
	ret
	.cfi_endproc
LFE39:
	.section .rdata,"dr"
LC17:
	.ascii "loop_soup\0"
LC18:
	.ascii "\11x is %d\12\12\0"
LC19:
	.ascii "\11Now x is %d\12\12\0"
LC20:
	.ascii "\11Finally, x is %d\12\12\0"
LC21:
	.ascii "\11I'm in an infinite loop\12\12\0"
LC22:
	.ascii "\11x is 17 now; Time to break\12\12\0"
	.text
	.globl	_loop_soup
	.def	_loop_soup;	.scl	2;	.type	32;	.endef
_loop_soup:
LFB40:
	.cfi_startproc
	pushl	%ebp
	.cfi_def_cfa_offset 8
	.cfi_offset 5, -8
	movl	%esp, %ebp
	.cfi_def_cfa_register 5
	subl	$40, %esp
	movl	$LC17, (%esp)
	call	_print_function_header
	movl	$1, -12(%ebp)
	jmp	L8
L9:
	movl	-12(%ebp), %eax
	leal	1(%eax), %edx
	movl	%edx, -12(%ebp)
	movl	%eax, 4(%esp)
	movl	$LC18, (%esp)
	call	_printf
L8:
	cmpl	$2, -12(%ebp)
	jle	L9
	movl	$0, -12(%ebp)
	jmp	L10
L11:
	movl	-12(%ebp), %eax
	movl	%eax, 4(%esp)
	movl	$LC19, (%esp)
	call	_printf
	addl	$1, -12(%ebp)
L10:
	cmpl	$10, -12(%ebp)
	jle	L11
L12:
	addl	$1, -12(%ebp)
	movl	-12(%ebp), %eax
	movl	%eax, 4(%esp)
	movl	$LC20, (%esp)
	call	_printf
	cmpl	$14, -12(%ebp)
	jle	L12
L16:
	movl	$LC21, (%esp)
	call	_printf
	addl	$1, -12(%ebp)
	cmpl	$17, -12(%ebp)
	jne	L19
	movl	$LC22, (%esp)
	call	_printf
	jmp	L18
L19:
	nop
	jmp	L16
L18:
	nop
	leave
	.cfi_restore 5
	.cfi_def_cfa 4, 4
	ret
	.cfi_endproc
LFE40:
	.section .rdata,"dr"
LC23:
	.ascii "terms_and_conditions\0"
LC24:
	.ascii "true\0"
LC25:
	.ascii "false\0"
LC26:
	.ascii "\11a is %s\12\12\0"
LC27:
	.ascii "\11Oh, actually, a is %s\12\12\0"
	.align 4
LC28:
	.ascii "\11Wait, no, a is seriously %s\12\12\0"
LC29:
	.ascii "\11a && b is %s\12\12\0"
LC30:
	.ascii "\11a || b is %s\12\12\0"
	.align 4
LC31:
	.ascii "\11Be careful of order of operations!\12\12\0"
LC32:
	.ascii "\11%d & %d != 0 is %s\12\12\0"
LC33:
	.ascii "\11(%d & %d) != 0 is %s\12\12\0"
LC34:
	.ascii "\11If you see this, a is true\12\12\0"
	.align 4
LC35:
	.ascii "\11If you see this, b is false\12\12\0"
LC36:
	.ascii "\11If you see this, b is true\12\12\0"
	.align 4
LC37:
	.ascii "\11If you see this, a is true, and b is false\12\12\0"
	.align 4
LC38:
	.ascii "\11If you see this, a is true, and b is true\12\12\0"
LC39:
	.ascii "\11If you see this, a != b\12\12\0"
LC40:
	.ascii "\11x doubled to %d\12\12\0"
	.align 4
LC41:
	.ascii "\11NEVER SHOULD HAVE COME HERE!\12\12\0"
	.text
	.globl	_terms_and_conditions
	.def	_terms_and_conditions;	.scl	2;	.type	32;	.endef
_terms_and_conditions:
LFB41:
	.cfi_startproc
	pushl	%ebp
	.cfi_def_cfa_offset 8
	.cfi_offset 5, -8
	movl	%esp, %ebp
	.cfi_def_cfa_register 5
	subl	$40, %esp
	movl	$LC23, (%esp)
	call	_print_function_header
	movb	$1, -9(%ebp)
	movb	$0, -10(%ebp)
	cmpb	$0, -9(%ebp)
	je	L21
	movl	$LC24, %eax
	jmp	L22
L21:
	movl	$LC25, %eax
L22:
	movl	%eax, 4(%esp)
	movl	$LC26, (%esp)
	call	_printf
	movzbl	-10(%ebp), %eax
	movb	%al, -9(%ebp)
	cmpb	$0, -9(%ebp)
	je	L23
	movl	$LC24, %eax
	jmp	L24
L23:
	movl	$LC25, %eax
L24:
	movl	%eax, 4(%esp)
	movl	$LC27, (%esp)
	call	_printf
	movb	$1, -9(%ebp)
	cmpb	$0, -9(%ebp)
	je	L25
	movl	$LC24, %eax
	jmp	L26
L25:
	movl	$LC25, %eax
L26:
	movl	%eax, 4(%esp)
	movl	$LC28, (%esp)
	call	_printf
	cmpb	$0, -9(%ebp)
	je	L27
	cmpb	$0, -10(%ebp)
	je	L27
	movl	$LC24, %eax
	jmp	L28
L27:
	movl	$LC25, %eax
L28:
	movl	%eax, 4(%esp)
	movl	$LC29, (%esp)
	call	_printf
	cmpb	$0, -9(%ebp)
	jne	L29
	cmpb	$0, -10(%ebp)
	je	L30
L29:
	movl	$LC24, %eax
	jmp	L31
L30:
	movl	$LC25, %eax
L31:
	movl	%eax, 4(%esp)
	movl	$LC30, (%esp)
	call	_printf
	movl	$LC31, (%esp)
	call	_printf
	movl	$4, -16(%ebp)
	movl	$6, -20(%ebp)
	cmpl	$0, -20(%ebp)
	setne	%al
	movzbl	%al, %eax
	andl	-16(%ebp), %eax
	testl	%eax, %eax
	je	L32
	movl	$LC24, %eax
	jmp	L33
L32:
	movl	$LC25, %eax
L33:
	movl	%eax, 12(%esp)
	movl	-20(%ebp), %eax
	movl	%eax, 8(%esp)
	movl	-16(%ebp), %eax
	movl	%eax, 4(%esp)
	movl	$LC32, (%esp)
	call	_printf
	movl	-16(%ebp), %eax
	andl	-20(%ebp), %eax
	testl	%eax, %eax
	je	L34
	movl	$LC24, %eax
	jmp	L35
L34:
	movl	$LC25, %eax
L35:
	movl	%eax, 12(%esp)
	movl	-20(%ebp), %eax
	movl	%eax, 8(%esp)
	movl	-16(%ebp), %eax
	movl	%eax, 4(%esp)
	movl	$LC33, (%esp)
	call	_printf
	cmpb	$0, -9(%ebp)
	je	L36
	movl	$LC34, (%esp)
	call	_printf
L36:
	movzbl	-10(%ebp), %eax
	xorl	$1, %eax
	testb	%al, %al
	je	L37
	movl	$LC35, (%esp)
	call	_printf
	jmp	L38
L37:
	cmpb	$0, -10(%ebp)
	je	L38
	movl	$LC36, (%esp)
	call	_printf
L38:
	cmpb	$0, -9(%ebp)
	je	L39
	movzbl	-10(%ebp), %eax
	xorl	$1, %eax
	testb	%al, %al
	je	L40
	movl	$LC37, (%esp)
	call	_printf
	jmp	L39
L40:
	movl	$LC38, (%esp)
	call	_printf
L39:
	movzbl	-9(%ebp), %eax
	cmpb	-10(%ebp), %al
	je	L41
	movl	$LC39, (%esp)
	call	_printf
L41:
	movl	$2, -24(%ebp)
	cmpl	$4, -24(%ebp)
	je	L42
	cmpl	$4, -24(%ebp)
	jg	L43
	cmpl	$3, -24(%ebp)
	je	L44
	cmpl	$3, -24(%ebp)
	jg	L43
	cmpl	$1, -24(%ebp)
	je	L45
	cmpl	$2, -24(%ebp)
	je	L46
	jmp	L43
L45:
	addl	$1, -24(%ebp)
	jmp	L47
L46:
	sall	-24(%ebp)
	movl	-24(%ebp), %eax
	movl	%eax, 4(%esp)
	movl	$LC40, (%esp)
	call	_printf
	jmp	L47
L44:
	movl	-24(%ebp), %eax
	movl	%eax, %edx
	shrl	$31, %edx
	addl	%edx, %eax
	sarl	%eax
	movl	%eax, -24(%ebp)
	jmp	L47
L42:
	subl	$2, -24(%ebp)
	jmp	L47
L43:
	movl	$LC41, (%esp)
	call	_printf
	nop
L47:
	nop
	leave
	.cfi_restore 5
	.cfi_def_cfa 4, 4
	ret
	.cfi_endproc
LFE41:
	.section .rdata,"dr"
LC42:
	.ascii "disarray\0"
LC43:
	.ascii "\11Setting array[%d] to %d\12\12\0"
	.align 4
LC44:
	.ascii "\11passed_arr[%d] == local_arr[%d] == %d\12\12\0"
	.align 4
LC45:
	.ascii "\11dynamic_arr has a size of %d\12\12\0"
	.align 4
LC46:
	.ascii "\11Now, dynamic_arr has a size of %d\12\12\0"
	.text
	.globl	_disarray
	.def	_disarray;	.scl	2;	.type	32;	.endef
_disarray:
LFB42:
	.cfi_startproc
	pushl	%ebp
	.cfi_def_cfa_offset 8
	.cfi_offset 5, -8
	movl	%esp, %ebp
	.cfi_def_cfa_register 5
	subl	$88, %esp
	movl	$LC42, (%esp)
	call	_print_function_header
	movl	$0, -12(%ebp)
	jmp	L49
L50:
	movl	-12(%ebp), %eax
	addl	$1, %eax
	movl	%eax, 8(%esp)
	movl	-12(%ebp), %eax
	movl	%eax, 4(%esp)
	movl	$LC43, (%esp)
	call	_printf
	movl	-12(%ebp), %eax
	leal	1(%eax), %edx
	movl	-12(%ebp), %eax
	movl	%edx, -64(%ebp,%eax,4)
	addl	$1, -12(%ebp)
L49:
	cmpl	$9, -12(%ebp)
	jle	L50
	cmpl	$10, 12(%ebp)
	jne	L51
	movl	$0, -16(%ebp)
	jmp	L52
L54:
	movl	-16(%ebp), %eax
	leal	0(,%eax,4), %edx
	movl	8(%ebp), %eax
	addl	%edx, %eax
	movl	(%eax), %edx
	movl	-16(%ebp), %eax
	movl	-64(%ebp,%eax,4), %eax
	cmpl	%eax, %edx
	jne	L53
	movl	-16(%ebp), %eax
	leal	0(,%eax,4), %edx
	movl	8(%ebp), %eax
	addl	%edx, %eax
	movl	(%eax), %eax
	movl	%eax, 12(%esp)
	movl	-16(%ebp), %eax
	movl	%eax, 8(%esp)
	movl	-16(%ebp), %eax
	movl	%eax, 4(%esp)
	movl	$LC44, (%esp)
	call	_printf
L53:
	addl	$1, -16(%ebp)
L52:
	movl	-16(%ebp), %eax
	cmpl	12(%ebp), %eax
	jl	L54
L51:
	movl	$40, (%esp)
	call	_malloc
	movl	%eax, -20(%ebp)
	cmpl	$0, -20(%ebp)
	jne	L55
	movl	$LC2, (%esp)
	call	_printf
	jmp	L48
L55:
	movl	$10, 4(%esp)
	movl	$LC45, (%esp)
	call	_printf
	movl	$80, 4(%esp)
	movl	-20(%ebp), %eax
	movl	%eax, (%esp)
	call	_realloc
	movl	%eax, -24(%ebp)
	cmpl	$0, -24(%ebp)
	jne	L57
	movl	$LC2, (%esp)
	call	_printf
	movl	-20(%ebp), %eax
	movl	%eax, (%esp)
	call	_free
	movl	$0, -20(%ebp)
	jmp	L48
L57:
	movl	-24(%ebp), %eax
	movl	%eax, -20(%ebp)
	movl	$20, 4(%esp)
	movl	$LC46, (%esp)
	call	_printf
	movl	-20(%ebp), %eax
	movl	%eax, (%esp)
	call	_free
	movl	$0, -20(%ebp)
L48:
	leave
	.cfi_restore 5
	.cfi_def_cfa 4, 4
	ret
	.cfi_endproc
LFE42:
	.section .rdata,"dr"
LC47:
	.ascii "disappointers\0"
LC48:
	.ascii "\11\0"
LC49:
	.ascii "%c\0"
LC50:
	.ascii "\12\11%s\12\0"
	.text
	.globl	_disappointers
	.def	_disappointers;	.scl	2;	.type	32;	.endef
_disappointers:
LFB43:
	.cfi_startproc
	pushl	%ebp
	.cfi_def_cfa_offset 8
	.cfi_offset 5, -8
	movl	%esp, %ebp
	.cfi_def_cfa_register 5
	subl	$40, %esp
	movl	$LC47, (%esp)
	call	_print_function_header
	movl	8(%ebp), %eax
	movl	%eax, -12(%ebp)
	movl	$LC48, (%esp)
	call	_printf
	jmp	L60
L61:
	movl	-12(%ebp), %eax
	movzbl	(%eax), %eax
	movsbl	%al, %eax
	movl	%eax, 4(%esp)
	movl	$LC49, (%esp)
	call	_printf
	addl	$1, -12(%ebp)
L60:
	movl	-12(%ebp), %eax
	movzbl	(%eax), %eax
	testb	%al, %al
	jne	L61
	movl	$0, -12(%ebp)
	movl	12(%ebp), %eax
	leal	-2(%eax), %edx
	movl	8(%ebp), %eax
	addl	%edx, %eax
	movb	$63, (%eax)
	movl	8(%ebp), %eax
	movl	%eax, 4(%esp)
	movl	$LC50, (%esp)
	call	_printf
	nop
	leave
	.cfi_restore 5
	.cfi_def_cfa 4, 4
	ret
	.cfi_endproc
LFE43:
	.section .rdata,"dr"
LC51:
	.ascii "struct_your_stuff\0"
LC52:
	.ascii "\11thing_two.x == %d\12\12\0"
LC53:
	.ascii "\11*thing_two.px == %d\12\12\0"
	.text
	.globl	_struct_your_stuff
	.def	_struct_your_stuff;	.scl	2;	.type	32;	.endef
_struct_your_stuff:
LFB44:
	.cfi_startproc
	pushl	%ebp
	.cfi_def_cfa_offset 8
	.cfi_offset 5, -8
	movl	%esp, %ebp
	.cfi_def_cfa_register 5
	subl	$56, %esp
	movl	$LC51, (%esp)
	call	_print_function_header
	movb	$88, -20(%ebp)
	movl	$13, -16(%ebp)
	leal	-20(%ebp), %eax
	addl	$4, %eax
	movl	%eax, -12(%ebp)
	movb	$79, -32(%ebp)
	movl	$7, -28(%ebp)
	leal	-20(%ebp), %eax
	addl	$4, %eax
	movl	%eax, -24(%ebp)
	movl	$12, -16(%ebp)
	movl	-28(%ebp), %eax
	movl	%eax, 4(%esp)
	movl	$LC52, (%esp)
	call	_printf
	movl	-24(%ebp), %eax
	movl	(%eax), %eax
	movl	%eax, 4(%esp)
	movl	$LC53, (%esp)
	call	_printf
	nop
	leave
	.cfi_restore 5
	.cfi_def_cfa 4, 4
	ret
	.cfi_endproc
LFE44:
	.globl	_insert_at_start_of_ll
	.def	_insert_at_start_of_ll;	.scl	2;	.type	32;	.endef
_insert_at_start_of_ll:
LFB45:
	.cfi_startproc
	pushl	%ebp
	.cfi_def_cfa_offset 8
	.cfi_offset 5, -8
	movl	%esp, %ebp
	.cfi_def_cfa_register 5
	subl	$40, %esp
	movl	$8, (%esp)
	call	_malloc
	movl	%eax, -12(%ebp)
	cmpl	$0, -12(%ebp)
	jne	L64
	movl	$LC2, (%esp)
	call	_printf
	movl	$0, %eax
	jmp	L65
L64:
	movl	-12(%ebp), %eax
	movl	12(%ebp), %edx
	movl	%edx, (%eax)
	movl	-12(%ebp), %eax
	movl	8(%ebp), %edx
	movl	%edx, 4(%eax)
	movl	-12(%ebp), %eax
L65:
	leave
	.cfi_restore 5
	.cfi_def_cfa 4, 4
	ret
	.cfi_endproc
LFE45:
	.section .rdata,"dr"
	.align 4
LC54:
	.ascii "linked_list_not_to_be_confused_with_zeldad_list\0"
LC55:
	.ascii "\11HEAD =>\0"
LC56:
	.ascii " %d =>\0"
LC57:
	.ascii " END\12\12\0"
LC58:
	.ascii "\11Deleting %d...\12\12\0"
	.text
	.globl	_linked_list_not_to_be_confused_with_zeldad_list
	.def	_linked_list_not_to_be_confused_with_zeldad_list;	.scl	2;	.type	32;	.endef
_linked_list_not_to_be_confused_with_zeldad_list:
LFB46:
	.cfi_startproc
	pushl	%ebp
	.cfi_def_cfa_offset 8
	.cfi_offset 5, -8
	movl	%esp, %ebp
	.cfi_def_cfa_register 5
	subl	$40, %esp
	movl	$LC54, (%esp)
	call	_print_function_header
	movl	$0, -16(%ebp)
	movl	$99, 4(%esp)
	movl	-16(%ebp), %eax
	movl	%eax, (%esp)
	call	_insert_at_start_of_ll
	movl	%eax, -16(%ebp)
	movl	$66, 4(%esp)
	movl	-16(%ebp), %eax
	movl	%eax, (%esp)
	call	_insert_at_start_of_ll
	movl	%eax, -16(%ebp)
	movl	$33, 4(%esp)
	movl	-16(%ebp), %eax
	movl	%eax, (%esp)
	call	_insert_at_start_of_ll
	movl	%eax, -16(%ebp)
	movl	-16(%ebp), %eax
	movl	%eax, -12(%ebp)
	movl	$LC55, (%esp)
	call	_printf
	jmp	L67
L68:
	movl	-12(%ebp), %eax
	movl	(%eax), %eax
	movl	%eax, 4(%esp)
	movl	$LC56, (%esp)
	call	_printf
	movl	-12(%ebp), %eax
	movl	4(%eax), %eax
	movl	%eax, -12(%ebp)
L67:
	cmpl	$0, -12(%ebp)
	jne	L68
	movl	$LC57, (%esp)
	call	_printf
	movl	-16(%ebp), %eax
	movl	%eax, -12(%ebp)
	movl	$0, -20(%ebp)
	jmp	L69
L70:
	movl	-12(%ebp), %eax
	movl	%eax, -20(%ebp)
	movl	-12(%ebp), %eax
	movl	4(%eax), %eax
	movl	%eax, -12(%ebp)
	movl	-20(%ebp), %eax
	movl	(%eax), %eax
	movl	%eax, 4(%esp)
	movl	$LC58, (%esp)
	call	_printf
	movl	-20(%ebp), %eax
	movl	%eax, (%esp)
	call	_free
	movl	$0, -20(%ebp)
L69:
	cmpl	$0, -12(%ebp)
	jne	L70
	nop
	nop
	leave
	.cfi_restore 5
	.cfi_def_cfa 4, 4
	ret
	.cfi_endproc
LFE46:
	.def	___main;	.scl	2;	.type	32;	.endef
	.section .rdata,"dr"
LC59:
	.ascii "main\0"
LC60:
	.ascii "quick_maths() result is %d\12\12\0"
LC61:
	.ascii "All done!\12\12\0"
	.text
	.globl	_main
	.def	_main;	.scl	2;	.type	32;	.endef
_main:
LFB47:
	.cfi_startproc
	pushl	%ebp
	.cfi_def_cfa_offset 8
	.cfi_offset 5, -8
	movl	%esp, %ebp
	.cfi_def_cfa_register 5
	andl	$-16, %esp
	subl	$112, %esp
	call	___main
	movl	$LC59, (%esp)
	call	_print_function_header
	movl	$5, 100(%esp)
	movl	$7, 96(%esp)
	movl	$0, 92(%esp)
	movl	$0, 108(%esp)
	jmp	L72
L73:
	movl	108(%esp), %eax
	leal	1(%eax), %edx
	movl	108(%esp), %eax
	movl	%edx, 52(%esp,%eax,4)
	addl	$1, 108(%esp)
L72:
	cmpl	$9, 108(%esp)
	jle	L73
	movl	$544024393, 25(%esp)
	movl	$1953701985, 29(%esp)
	movl	$1735289202, 33(%esp)
	movl	$1869357100, 37(%esp)
	movl	$1629514607, 41(%esp)
	movl	$1701650548, 45(%esp)
	movl	$663909, 48(%esp)
	movl	$0, 104(%esp)
	movl	$0, 104(%esp)
	jmp	L74
L75:
	addl	$1, 104(%esp)
L74:
	leal	25(%esp), %edx
	movl	104(%esp), %eax
	addl	%edx, %eax
	movzbl	(%eax), %eax
	testb	%al, %al
	jne	L75
	movl	96(%esp), %eax
	movl	%eax, 4(%esp)
	movl	100(%esp), %eax
	movl	%eax, (%esp)
	call	_quick_maths
	movl	%eax, 4(%esp)
	movl	$LC60, (%esp)
	call	_printf
	call	_loop_soup
	call	_terms_and_conditions
	movl	$10, 4(%esp)
	leal	52(%esp), %eax
	movl	%eax, (%esp)
	call	_disarray
	movl	104(%esp), %eax
	movl	%eax, 4(%esp)
	leal	25(%esp), %eax
	movl	%eax, (%esp)
	call	_disappointers
	call	_struct_your_stuff
	call	_linked_list_not_to_be_confused_with_zeldad_list
	movl	$LC61, (%esp)
	call	_printf
	call	_getchar
	movl	$0, %eax
	leave
	.cfi_restore 5
	.cfi_def_cfa 4, 4
	ret
	.cfi_endproc
LFE47:
	.ident	"GCC: (Rev1, Built by MSYS2 project) 12.2.0"
	.def	___mingw_vfprintf;	.scl	2;	.type	32;	.endef
	.def	_malloc;	.scl	2;	.type	32;	.endef
	.def	_free;	.scl	2;	.type	32;	.endef
	.def	_realloc;	.scl	2;	.type	32;	.endef
	.def	_getchar;	.scl	2;	.type	32;	.endef
