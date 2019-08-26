import sys, os, re
import time

from itertools import permutations
import random

from PIL import Image
import pil_rgb_hsv_converter_v0_0 as rgbhsv
import pil_hsv_control_v0_0 as hsvcontrol

def get_sys_arg(arg):
	# path, prefix, color(list)
	color_list = list()
	for i in range(len(arg)):
		if i==0:
			continue
		elif i==1:
			directory = sys.argv[i]
		elif i==2:
			prefix = sys.argv[i]
		else:
			color_list.append(sys.argv[i])

	return directory, prefix, color_list

def hex_color_to_RGB(hex_color):
	r = int(hex_color[1:3], 16)
	g = int(hex_color[3:5], 16)
	b = int(hex_color[5:7], 16)
	return (r, g, b)


def get_palette_from_hue_list(hue_list, n_of_images, limit=1):
	hue_permutations = permutations(hue_list, n_of_images)
	hue_permutations_list = [i for i in hue_permutations]

	try:
		palette_list = random.sample(hue_permutations_list, limit)
	except ValueError as e:
		print(e)
		palette_list = random.sample(hue_permutations_list, len(hue_permutations_list))

	return palette_list


def get_max_size_of_images(_dir, _images):
	max_size = [0, 0]

	for each_image in _images:
		with Image.open(_dir+'/'+each_image) as im:
			size = im.size
			for i in range(2):
				if max_size[i] < size[i]:
					max_size[i] = size[i]

	return tuple(max_size)

def get_average_color_from_image(image):
	size = image.size
	px = image.load()

	average_color = [0, 0, 0]
	pixel_count = 0
	transparent = 0

	for i in range(size[0]):
		for j in range(size[1]):
			if px[i, j][3] != transparent:
				pixel_count += 1
				for k in range(len(average_color)):
					average_color[k] += px[i, j][k]

	average_color = [round(each / pixel_count) for each in average_color]


	return tuple(average_color)

def change_average_color_of_image_to_specific_hue(image, hue):
	average_color = get_average_color_from_image(image)
	hsv_of_average_color = rgbhsv.rgb_to_hsv(average_color)

	degree_to_rotate = hue - hsv_of_average_color[0]

	size = image.size
	px = image.load()
	transparent = 0

	for i in range(size[0]):
		for j in range(size[1]):
			if px[i, j][3] != transparent:
				rgb = px[i, j][0:3]
				new_rgb = hsvcontrol.pixel_rotate_hue(rgb, degree_to_rotate)
				px[i, j] = (new_rgb[0], new_rgb[1], new_rgb[2], px[i, j][3])


def main():
	start = time.time()
	if len(sys.argv) == 1:
		directory='../uploads/20200708172148325'
		prefix='test_prefix'
		color_list=['#ffff00', '#00ffff', '#ff00ff', '#ff0000']
	else:
		directory, prefix, color_list = get_sys_arg(sys.argv)

	# listing original images
	pattern = re.compile(prefix + '_original_\d+\.png')
	base_images = [each_file_name for each_file_name in os.listdir(directory) if pattern.match(each_file_name)]

	#hue_list = [rgbhsv.rgb_to_hsv(hex_color_to_RGB(each_color))[0] for each_color in color_list]
	color_list = [hex_color_to_RGB(each_color) for each_color in color_list]
	hue_list = [rgbhsv.rgb_to_hsv(each_rgb)[0] for each_rgb in color_list]

	# only for sample
	palette_permutations = get_palette_from_hue_list(hue_list=hue_list, n_of_images=len(base_images), limit=3)

	# get size of merged image
	merged_size = get_max_size_of_images(directory, base_images)


	# main!
	for i in range(len(palette_permutations)):
		with Image.new('RGBA', merged_size) as merged_im:
			for j in range(len(base_images)):
				with Image.open(directory + '/' + base_images[j]) as im:
					change_average_color_of_image_to_specific_hue(im, palette_permutations[i][j])
					merged_im.paste(im, (0, 0), im)
			merged_im.save('%s/%s_%03d.png' % (directory, prefix, i))

	with Image.new('RGBA', merged_size) as original_im:
		for j in range(len(base_images)):
			with Image.open(directory + '/' + base_images[j]) as im:
				original_im.paste(im, (0, 0), im)
		original_im.save('%s/original.png' % (directory))


	print('converting took %d second(s)' % round(time.time() - start))



if __name__ == '__main__':
	main()































