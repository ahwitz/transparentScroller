from __future__ import division
from math import floor
import os, sys
import argparse
import re

from PIL import Image
from pgmagick import Image as mImage, ImageList

#alpha 0 is true transparent\

parser = argparse.ArgumentParser(description='Creates a transparent video scrolling through a pdf.')
parser.add_argument('-t', '--temp', metavar='t', nargs=1, help='temp directory')
parser.add_argument('input', metavar='i', nargs='*', help='input file')
args = parser.parse_args()
args.temp = args.temp[0]

pdf = False
png = False
type = ""
images = []
for file in args.input:
	if len(re.findall("\.pdf", file)) > 0:
		pdf = True
	elif len(re.findall("\.png", file)) > 0:
		png = True
	else:
		print "File type must be png or pdf, and all files must have the same extension."
		sys.exit(1)

if pdf == png:
	print "File type must be png or pdf, and all files must have the same extension."
        sys.exit(1)
elif pdf:
    type = "pdf"
elif png:
    type = "png"

if not os.path.exists(args.temp):
    os.makedirs(args.temp)
else:
    print "It looks like the movie file already exists in this folder and there may be another copy of this script running. To avoid any kind of overlap, please make sure there's no directory named", args.temp, "in /Users/vp2/VideoProd_Assets/TransparentScrollerScript/" 
    sys.exit(1)

if type == "pdf":
	if not os.path.exists(args.input):
	    print "Input file does not exist."
	    sys.exit(1)

	mimage = mImage()
	mimage.density("100")
	mimage.quality(100)
	try:
		mimage.read(args.input)
	except RuntimeError:
		print "ImageMagick threw an error. Make sure the filename is correct."
		sys.exit()
	print "ImageMagick is converting to png..."
	mimage.write(args.temp + '/temp.png')

	print "Loading into PIL..."
	images[0] = Image.open(args.temp + "/temp.png")

else:
	images = [Image.open(a) for a in args.input]

pix_arr = {}
pix_arr_height = 0
for image in images:
	print "Loading", image.filename
	sequence = []
	pix_arr_orig = image.load()
	img_x, img_y = image.size
	for x in range(img_x):
		for y in range(img_y):
			pix_arr[x, pix_arr_height + y] = pix_arr_orig[x, y]
	pix_arr_height = pix_arr_height + img_y	

print "Total height of scrolled text:", pix_arr_height, pix_arr[0, pix_arr_height - 1]
new_img_height = int((img_x / 16) * 9)
rgba = (len(pix_arr[0,0]) == 4)

print "Inverting image..."
if rgba:
	def convert_pix(tuple):
		if tuple[3] == (0):
			return (0,0,0,0)
		elif tuple[0:3] == (0, 0, 0):
 			return (255, 255, 255, 255)
		else:
			return pix_arr[x, y]
else:
	def convert_pix(tuple):			
		if tuple == (255, 255, 255):
			return (0, 0, 0, 0)
		elif tuple == (0, 0, 0):
			return (255, 255, 255, 255)
		else:
			return pix_arr[x, y] + (0,)

print "Saving frames..."

new_img = Image.new("RGBA", (img_x, new_img_height))
new_img_pix = new_img.load()
for cur_x in range(img_x):
	for cur_y in range(new_img_height - 1):
		new_img_pix[cur_x, cur_y] = convert_pix(pix_arr[cur_x, cur_y])

for cur_start_pos in range(0, pix_arr_height - new_img_height):
	start_pos_string = str(cur_start_pos)
 	while len(start_pos_string) < 5:
 		start_pos_string = "0" + start_pos_string
	
 	new_img.save(args.temp + "/frame" + start_pos_string + ".png")
 	if cur_start_pos % 10 == 0:
 		print "Created", cur_start_pos, "out of", (pix_arr_height - new_img_height), "images."
	
	for cur_x in range(img_x):
		for cur_y in range(1, new_img_height):                
			new_img_pix[cur_x, cur_y - 1] = new_img_pix[cur_x, cur_y]
	
	for cur_x in range(img_x):
		new_img_pix[cur_x, new_img_height - 1] = convert_pix(pix_arr[cur_x, cur_start_pos + new_img_height])


start_pos_string = str(cur_start_pos)
while len(start_pos_string) < 5:
        start_pos_string = "0" + start_pos_string

new_img.save(args.temp + "/frame" + start_pos_string + ".png")
