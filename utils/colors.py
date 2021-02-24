from math import sqrt

def hexcol_to_int(inp:str):
	if inp.startswith("#"):
		inp = inp[1:]

	if len(inp) == 3:
		inp = ''.join(map(lambda x:2*x, inp.split('')))

	R = int(inp[:2], 16)
	G = int(inp[2:4], 16)
	B = int(inp[4:], 16)

	return R,G,B

def int_to_hexcol(r:int,g:int,b:int):
	def pad_hex(inp:int):
		return hex(inp)[2:].rjust(2, "0")

	return f"#{pad_hex(r)}{pad_hex(g)}{pad_hex(b)}"

def _transform(inp:str, r,g,b):
	R,G,B = hexcol_to_int(inp)
	return int_to_hexcol(abs(R+r)%255, abs(G+g)%255, abs(B+b)%255)

def add(inp:str, mod:str):
	return _transform(inp, *hexcol_to_int(mod))

def subtract(inp:str, mod:str):
	return _transform(inp, *map(lambda x:-x, hexcol_to_int(mod)))

def grayscale(inp:str, bias:float=1.0):
	R,G,B = hexcol_to_int(inp)
	GS = int(sqrt((R**2 + G**2 + B**2) / 3))
	R = int(GS*bias+(1-bias)*R)
	G = int(GS*bias+(1-bias)*G)
	B = int(GS*bias+(1-bias)*B)
	return int_to_hexcol(R, G, B)
