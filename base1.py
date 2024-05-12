import os
from PIL import Image
from PIL import ImageFilter, ImageEnhance

#output_name = input('output name : ')

path = './source/'
imgs = os.listdir(path)

temp = []
for img in imgs:
	if '.png' in img:
		temp.append(img)
print(temp)

imgs = [path + img for img in temp]
images = [Image.open(img) for img in imgs]

max_width = max([img.size[0] for img in images])
max_height = max([img.size[1] for img in images])

images = [img.resize((max_width, max_height), Image.BICUBIC) for img in images]
images = [img.filter(ImageFilter.EDGE_ENHANCE) for img in images]
images = [ImageEnhance.Color(img).enhance(2) for img in images]
#images = [img.filter(ImageFilter.MinFilter(5)) for img in images]


durate = 500
#durate = float(image_fps.get())*1000

im = images[0]
im.save('./output/{}.gif'.format('output'), save_all=True, append_images=images[1:], loop=0xff, duration=durate)


print('image count : {count}, output size : ({width}, {height}), duration : {duration}s'.format(count=len(images), width=max_width, height=max_height, duration=durate/1000))
