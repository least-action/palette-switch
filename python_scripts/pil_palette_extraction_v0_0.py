from PIL import Image
import math
import os

'''
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


def rgb_to_hsv(rgb):
	M = max(rgb)
	m = min(rgb)
	diff = M - m
	
	if diff == 0:
		hue = 0
	elif M == rgb[0]:
		hue = 0 + 60 * ((rgb[1]-rgb[2]) / diff)
		if hue < 0:
			hue = 360 + hue
	elif M == rgb[1]:
		hue = 120 + 60 * ((rgb[2]-rgb[0]) / diff)
	elif M == rgb[2]:
		hue = 240 + 60 * ((rgb[0]-rgb[1]) / diff)

	if M == 0:
		sat = 0
	else:
		sat = diff / M * 100
	
	val = 1/255 * M * 100

	
	hsv = [round(hue), round(sat), round(val)]
	# print('hsv:', hsv)

	return hsv
'''


def get_evenly_divided_hsv_based_palette_from_image(image, hue_divide=10, sat_divide=5, val_divide=5, num_of_palette=1):
	if num_of_palette > hue_divide * sat_divide * val_divide:
		print("set number of palette less then divided area")
		return None
	elif hue_divide * sat_divide * val_divide == 0:
		print("set deivde bigger than zero")
		return None

	hsv_palette = list()
	section_count = list()
	
	for i in range(hue_divide):
		hsv_palette.append([])
		section_count.append([])
		for j in range(sat_divide):
			hsv_palette[i].append([])
			section_count[i].append([])
			for k in range(val_divide):
				hsv_palette[i][j].append([0, 0, 0])
				section_count[i][j].append(0)

	size = image.size
	px = image.load()


	for i in range(size[0]):
		for j in range(size[1]):
			hsv = rgb_to_hsv(px[i, j])
			if hsv[0] == 360:
				hue_section = hue_divide-1
			else:
				hue_section = int(hsv[0] / (360 / hue_divide))
			if hsv[1] == 100:
				sat_section = sat_divide-1
			else:
				sat_section = int(hsv[1] / (100 / sat_divide))
			if hsv[2] == 100:
				val_section = val_divide-1
			else:
				val_section = int(hsv[2] / (100 / val_divide))


			section_count[hue_section][sat_section][val_section] += 1 * (sat_section ** 2)
			for k in range(3):
				hsv_palette[hue_section][sat_section][val_section][k] += hsv[k] * (sat_section ** 2)

	for i in range(hue_divide):
		for j in range(sat_divide):
			for k in range(val_divide):
				for l in range(3):
					if section_count[i][j][k] == 0:
						continue
					hsv_palette[i][j][k][l] = round(hsv_palette[i][j][k][l] / section_count[i][j][k])


	# hsv_palette = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]

	# print(section_count)
	# print(hsv_palette)

	one_dim_count = list()
	one_dim_palette = list()

	for i in range(hue_divide):
		for j in range(sat_divide):
			for k in range(val_divide):
				one_dim_count.append(section_count[i][j][k])
				one_dim_palette.append(hsv_to_rgb(hsv_palette[i][j][k]))

	# print(one_dim_count)
	# print(one_dim_palette)

	top_index = sorted(range(len(one_dim_count)), key=lambda i: one_dim_count[i], reverse=True)

	top_palette = list()
	for i in range(num_of_palette):
		top_palette.append(one_dim_palette[top_index[i]])

	
	return top_palette



def main():
	directory = '/var/www/html/palette/images'
	filename = '/balls/balls.jpg'
	filename = directory + filename

	palette_list = list()
	num = 15

	with Image.open(filename) as im:
		size = im.size
		#palette_list = get_evenly_divided_hsv_based_palette_from_image(im, hue_divide=10, sat_divide=1, val_divide=1, num_of_palette=num)
		palette_list = get_evenly_divided_hsv_based_palette_from_image(im, num_of_palette=num)

	
	height = 50
	width = num * height

	# print(palette_list)

	with Image.new('RGB', (width, height)) as p_im:
		size = p_im.size

		px = p_im.load()

		for i in range(size[0]):
			for j in range(size[1]):
				px[i, j] = tuple(palette_list[i//height])


		p_im.save('%s_b_palette_%02d.jpg' % (os.path.splitext(filename)[0], num), 'JPEG')
	# print(hsv_to_rgb(rgb_to_hsv((42, 183, 201))))


if __name__ == '__main__':
	main()


