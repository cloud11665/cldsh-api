

style = hex(0b0_1_1_1_01_110_110)
print(style)
style = int(style, 16)

subject_style =      (style&0x800)>>11
time_enabled =       (style&0x400)>>10
time_unit =          (style&0x200)>>9
time_display_unit =  (style&0x100)>>8
time_separator =     [" ", ":", ".", "/"][((style&0xc0)>>6) % 4]
time_bracket_begin = ["<", "{", "[", "(", ""][((style&0x38)>>3) % 5]
time_bracket_end   = [">", "}", "]", ")", ""][((style&0x07)>>0) % 5]

print(subject_style)
print(time_enabled)
print(time_unit)
print(time_display_unit)
print(time_separator)
print(time_bracket_begin)
print(time_bracket_end)

'''

		- subject style (1)
		- time (1)
		- time_unit [minutes/hours] (1)
		- time_display_unit (1)
		- time_separator [" ", ":", ".", "/"] (2)
		- time_bracket_begin ["<", "{", "[", "(", ""] (3)
		- time_bracket_end   [">", "}", "]", ")", ""] (3)
??=define

int main() ??<
	struct* foo;

	foo.*
	foo->*

	_Alignof

	<=>

	return 0;
??>

'''
#bytemap = [(style >> i & 0xff) for i in (16,8,0)]
#print([bin(x) for x in bytemap])

#print(bytearray(2))
#print(bytes(2))
#print(bytes(int(style, 16)))
#bitmask = bytearray.fromhex(style)