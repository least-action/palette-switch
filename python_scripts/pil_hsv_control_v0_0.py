from PIL import Image

def pixel_rotate_hue(rgb_code, degree):
	test = False
	degree = degree % 360
	new_rgb = [rgb_code[0], rgb_code[1], rgb_code[2]]

	M = max(new_rgb)
	m = min(new_rgb)
	tmp = list(new_rgb)
	tmp.remove(M)
	mid = max(tmp)
	
	if M == m:
		return tuple(new_rgb)

	pixel_to_move = round(degree * (M - m) / 60)

	rotate_120 = pixel_to_move // (2 * (M - m))
	rotate_60 = (pixel_to_move % (2 * (M - m))) // (M - m)
	rotate_tip = pixel_to_move % (M - m)
	if test:
		print('120:', rotate_120)
		print(' 60:', rotate_60)
		print('tip:', rotate_tip)
		print(new_rgb)

	for i in range(rotate_120):
		aux = list(new_rgb)
		new_rgb[0] = aux[2]
		new_rgb[1] = aux[0]
		new_rgb[2] = aux[1]
	if test:
		print('step1:', new_rgb)

	if rotate_60 == 1:
		if new_rgb.count(M) == 2:
			new_rgb[new_rgb.index(m)-2] = m
		elif new_rgb.count(m) == 2:
			new_rgb[new_rgb.index(M)-2] = M
		elif (new_rgb.index(m) == new_rgb.index(M) + 1) or (new_rgb.index(m) == new_rgb.index(M) - 2):
			max_index = new_rgb.index(M)
			new_rgb[max_index-1] = m
			new_rgb[max_index-2] = m + (M - mid)
		else:
			max_index = new_rgb.index(M)
			new_rgb[max_index-2] = M
			new_rgb[max_index] = M - (mid - m)
	if test:
		print('step2:', new_rgb)

	M = max(new_rgb)
	m = min(new_rgb)
	tmp = list(new_rgb)
	tmp.remove(M)
	mid = max(tmp)

	if rotate_tip == 0:
		pass
	else:
		if new_rgb.count(M) == 2:
			new_rgb[new_rgb.index(m)-2] = M - rotate_tip
		elif new_rgb.count(m) == 2:
			new_rgb[new_rgb.index(M)-2] = m + rotate_tip
		elif (new_rgb.index(m) == new_rgb.index(M) + 1) or (new_rgb.index(m) == new_rgb.index(M) - 2):
			if rotate_tip < mid - m:
				new_rgb[new_rgb.index(M)-1] = mid - rotate_tip
			else:
				new_rgb[new_rgb.index(M)-1] = m
				new_rgb[new_rgb.index(M)-2] = m + rotate_tip - (mid - m)
		else:
			if rotate_tip < M - mid:
				new_rgb[new_rgb.index(M)-2] = mid + rotate_tip
			else:
				max_index = new_rgb.index(M)
				new_rgb[max_index-2] = M
				new_rgb[max_index] = M - (rotate_tip - (M - mid))


	if test:
		print('step3:', new_rgb)

	return tuple(new_rgb)


def image_rotate_hue(image, degree):
	if degree == 0:
		return
	else:
		degree = degree % 360
	size = image.size
	px = image.load()
	for i in range(size[0]):
		for j in range(size[1]):
			px[i, j] = pixel_rotate_hue(px[i, j], degree)


def saturation_control(image, percent):
	if percent < -100:
		percent = -100
	size = image.size
	px = image.load()
	for i in range(size[0]):
		for j in range(size[1]):
			if percent == 0:
				pass
			else:
				M = max(px[i, j])
				px[i, j] = tuple(max(round(px[i, j][each] + (px[i, j][each] - M) * percent / 100), 0) for each in range(3))

def saturation_control_incease_based_max_s(image, percent):
	if percent == 0:
		return
	elif percent < -100:
		percent = -100
	elif percent > 100:
		percent = 100
	size = image.size
	px = image.load()
	for i in range(size[0]):
		for j in range(size[1]):
			if percent < 0:
				M = max(px[i, j])
				px[i, j] = tuple(max(round(px[i, j][each] + (px[i, j][each] - M) * percent / 100), 0) for each in range(3))
			else:
				M = max(px[i, j])
				m = min(px[i, j])
				if M == m:
					pass
				else:
					px[i, j] = tuple([round(px[i, j][each] + ((px[i, j][each] - M) * m / (M - m)) * percent / 100) for each in range(3)])


def value_control(image, percent):
	if percent == 0:
		return
	elif percent < -100:
		percent = -100
	size = image.size
	px = image.load()
	for i in range(size[0]):
		for j in range(size[1]):
			px[i, j] = tuple([min(round(px[i, j][each] * (100 + percent) / 100), 255) for each in range(3)])

def value_control_increase_based_max_v(image, percent):
	if percent == 0:
		return
	elif percent < -100:
		percent = -100
	elif percent > 100:
		percent = 100
	size = image.size
	px = image.load()
	for i in range(size[0]):
		for j in range(size[1]):
			if percent < 0:
				px[i, j] = tuple([round(px[i, j][each] * (100 + percent) / 100) for each in range(3)])

			else:
				M = max(px[i, j])
				ratio = (1 + (255 / M - 1) * percent / 100)
				px[i, j] = tuple([min(round(px[i, j][each] * ratio), 255) for each in range(3)])


def main():
	print("pil_hsv_control.py main function executed")
	directory = '/var/www/html/palette/images/'
	filename = '/balls/balls.jpg'
	filename = directory + filename

	#import os
	# value version 1
#	for percent in [-100, -50, 0, 100, 200, 500, 999999]:
#		with Image.open(filename) as im:
#			value_control(im, percent)
#			im.save("%s_value_control_%03d.jpg" % (os.path.splitext(filename)[0], percent), "JPEG")
	
	# value version 2
#	for percent in range(-100, 100+1, 50):
#		with Image.open(filename) as im:
#			value_control_increase_based_max_v(im, percent)
#			im.save("%s_value_control_increase_based_max_v_%03d.jpg" % (os.path.splitext(filename)[0], percent), "JPEG")


	# saturation version 1
#	for percent in [-100, -50, 0, 100, 200, 500, 999999]:
#		with Image.open(filename) as im:
#			saturation_control(im, percent)
#			im.save("%s_saturation_control_%03d.jpg" % (os.path.splitext(filename)[0], percent), "JPEG")

	# saturation version 2
#	for percent in range(-100, 100+1, 50):
#		with Image.open(filename) as im:
#			saturation_control_incease_based_max_s(im, percent)
#			im.save("%s_saturation_control_incease_based_max_s_%03d.jpg" % (os.path.splitext(filename)[0], percent), "JPEG")


	# hue
	#for degree in range(0, 360+1, 20):
	#for degree in [360]:
	#	with Image.open(filename) as im:
	#		image_rotate_hue(im, degree)
	#		im.save("%s_image_rotate_hue_%03d_degree.jpg" % (os.path.splitext(filename)[0], degree), "JPEG")

	# a = (244, 0, 254)
	# for i in [10 * i for i in range(12)]:
	# 	ne = pixel_rotate_hue(a, i)
	# 	print('%3d  [%3d, %3d, %3d]' % (i, ne[0], ne[1], ne[2]))

	# print(pixel_rotate_hue(a, 60))



if __name__ == '__main__':
	main()


