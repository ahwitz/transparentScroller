from __future__ import division
from math import floor
import os, sys
import argparse

from PIL import Image
from pgmagick import Image as mImage, ImageList

#alpha 0 is true transparent\

parser = argparse.ArgumentParser(description='Creates a transparent video scrolling through a pdf.')
parser.add_argument('input', metavar='i', help='input file')
args = parser.parse_args()

if not os.path.exists('imgout'):
    os.makedirs('imgout')

mimage = mImage()
mimage.density("100")
mimage.quality(100)
try:
	mimage.read(args.input)
except RuntimeError:
	print "ImageMagick threw an error. Make sure the filename is correct."
	sys.exit()
print "ImageMagick is converting to png..."
mimage.write('imgout/temp.png')

print "Loading into PIL..."
image = Image.open('imgout/temp.png')

sequence = []
pix_arr = image.load()
img_x, img_y = image.size
#convert to 16*9
new_img_height = int((img_x / 16) * 9)

for cur_start_pos in range(0, img_y - new_img_height):
 	new_img = Image.new("RGBA", (img_x, new_img_height))
 	new_img_pix = new_img.load()
 	for x in range(img_x):
 		for y in range(new_img_height):
 			new_img_pix[x, y] = pix_arr[x, cur_start_pos + y]

 	start_pos_string = str(cur_start_pos)
 	while len(start_pos_string) < 5:
 		start_pos_string = "0" + start_pos_string

 	new_img.save("imgout/frame" + start_pos_string + ".png")
 	if cur_start_pos % 10 == 0:
 		print "Created", cur_start_pos, "out of", (img_y - new_img_height), "images."