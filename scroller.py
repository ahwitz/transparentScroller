from __future__ import division
from PIL import Image
from math import floor
import os
from pgmagick import Image as mImage, ImageList
#import cv2, cv

#mimage = MagickImage('test.pdf')
#mimageout = mimage.write('test.png')

#alpha 0 is true transparent\

if not os.path.exists('imgout'):
    os.makedirs('imgout')

mimage = mImage()
mimage.density("200")
mimage.quality(100)
mimage.read('test.pdf')
mimage.write('imgout/temp.png')

image = Image.open('imgout/temp.png')

sequence = []
pix_arr = image.load()
img_x = 1274
img_y = image.size[1]
new_img_height = int(floor((img_y / 16) * 9))

for cur_start_pos in range(0, img_y - new_img_height):
 	new_img = Image.new("RGBA", (img_x, new_img_height))
 	new_img_pix = new_img.load()
 	for x in range(img_x):
 		for y in range(new_img_height):
 			new_img_pix[x, y] = pix_arr[x, cur_start_pos + y]

 	start_pos_string = str(cur_start_pos)
 	while len(start_pos_string) < 5:
 		start_pos_string = "0" + start_pos_string

 	new_img.save("imgout/image" + start_pos_string + ".png")
 	if cur_start_pos % 10 == 0:
 		print "Created", cur_start_pos, "out of", (img_y - new_img_height), "images."