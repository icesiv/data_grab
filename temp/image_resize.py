import PIL
from PIL import Image


img = Image.open('temp/fullsized_image.png')
basewidth = int(img.size[0] + (img.size[0] * .1))
wpercent = (basewidth / float(img.size[0]))
hsize = int((float(img.size[1]) * float(wpercent)))
img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
img.save('temp/resized_image.png')