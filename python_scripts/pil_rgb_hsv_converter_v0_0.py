def rgb_to_hsv(rgb):
	tmp_rgb = [rgb[0], rgb[1], rgb[2]]

	M = max(tmp_rgb)
	m = min(tmp_rgb)
	diff = M - m
	
	if diff == 0:
		hue = 0
	elif M == tmp_rgb[0]:
		hue = 0 + 60 * ((tmp_rgb[1]-tmp_rgb[2]) / diff)
		if hue < 0:
			hue = 360 + hue
	elif M == tmp_rgb[1]:
		hue = 120 + 60 * ((tmp_rgb[2]-tmp_rgb[0]) / diff)
	elif M == tmp_rgb[2]:
		hue = 240 + 60 * ((tmp_rgb[0]-tmp_rgb[1]) / diff)

	if M == 0:
		sat = 0
	else:
		sat = diff / M * 100
	
	val = 1/255 * M * 100

	hsv = [round(hue), round(sat), round(val)]

	return hsv

def hsv_to_rgb(hsv):
	rgb = [0, 0, 0]

	hue, sat, val = hsv[0], hsv[1], hsv[2]

	M = 255 * val / 100

	if M == 0:
		return [0, 0, 0]
	steps_from_red = (hue / 60) * M

	num_of_side = int(steps_from_red / (2 * M))
	remainder = steps_from_red - num_of_side * 2 * M

	if remainder > M:
		remainder -= M
		rgb = [M - sat / 100 * remainder, M, M * (1 - sat / 100)]
	else:
		rgb = [M, M - (M - remainder) * sat / 100, M * (1 - sat / 100)]

	if num_of_side == 2:
		tmp = rgb[0]
		rgb[0] = rgb[1]
		rgb[1] = rgb[2]
		rgb[2] = tmp
	elif num_of_side == 1:
		tmp = rgb[0]
		rgb[0] = rgb[2]
		rgb[2] = rgb[1]
		rgb[1] = tmp
	else:
		pass

	for i in range(3):
		rgb[i] = round(rgb[i])

	return rgb

def main():
	pass

if __name__ == '__main__':
	main()






















