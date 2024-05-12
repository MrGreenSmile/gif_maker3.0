import os, sys

import cv2
from PIL import Image

from tkinter import Tk, scrolledtext
from tkinter.ttk import Combobox
from tkinter import filedialog, Button, Entry, Label


if not os.path.isdir('./output/'):
	os.mkdir('./output')
	print('directory prepared.')

def image_opener():
	global gif_state
	gif_state = 'image'

	img = filedialog.askopenfilenames(filetypes=[('images', '*.jpg;*.jpeg;*.png;'), ('any file', '*.*')], initialdir='./source/')
	
	scrolled.configure(state="normal")
	scrolled.delete("1.0", "end")

	for im in img:
		scrolled.insert("end", '-%s\n' % im)

def video_opener():
	global gif_state
	gif_state = 'video'

	img = filedialog.askopenfilename(filetypes=[('videos', '*.mp4;*.wmv;*.avi;'), ('any file', '*.*')], initialdir='./source/')
	
	scrolled.configure(state="normal")
	scrolled.delete("1.0", "end")
	scrolled.insert("1.0", img)
	scrolled.configure(state="disabled")
	print(img)

def gif_maker():
	if gif_state == 'image':
		temp_imgs = scrolled.get("1.0", "end")
		temp_imgs = temp_imgs.split('\n')
		imgs = []
		for img in temp_imgs:
			if not img == "":
				img = img[1:]
				imgs.append(img)
		images = [Image.open(img) for img in imgs]

		max_width = max([img.size[0] for img in images])
		max_height = max([img.size[1] for img in images])

		images = [img.resize((max_width, max_height)) for img in images]

		durate = float(image_fps.get())*1000

		img = images[0]
		img.save('./output/{}.gif'.format(output_name.get()), save_all=True, append_images=images[1:], loop=0xff, duration=durate)

		print('process done. {count} images, output size : ({width}, {height}), duration : {duration}s.'.format(count=len(images), width=max_width, height=max_height, duration=durate/1000))

	if gif_state == 'video':
		temp_imgs = scrolled.get("1.0", "end").split('\n')
		Vcap = cv2.VideoCapture(temp_imgs[0])

		start_sec = int(vid_btw_str.get())
		end_sec = int(vid_btw_stp.get())
		frame_count = int(Vcap.get(cv2.CAP_PROP_FRAME_COUNT))
		if vid_fps.get() == "fps":
			fps = round(Vcap.get(cv2.CAP_PROP_FPS))
		else:
			fps = float(vid_fps.get())
		d_start = start_sec * fps
		d_end = end_sec * fps

		durate = (d_end/fps - d_start/fps)
		print(frame_count)
		print(fps)
		print(durate)


		ret, frame = Vcap.read()

		images = []
		f = 0
		while ret:
			f += 1
			if d_start <= f <= d_end:
				images.append(frame)
			ret, frame = Vcap.read()

		Vcap.release()

		images = [Image.fromarray(img) for img in images]
		image = images[0]
		image.save('./output/{}.gif'.format(output_name.get()), save_all=True, append_images=images[1:], loop=0xff, duration=durate)

		print('process done. source : {video_name}, duration : {duration}s.'.format(video_name=temp_imgs[0].split('/')[-1], duration=durate))


window = Tk()
window.title('GIF Maker 3.0.0')
window.geometry('350x250+150+150')
window.resizable(False, False)
if os.path.isfile('./icon.ico'):
	window.iconbitmap('./icon.ico')


output_lbl = Label(window, text='output name : ')
output_lbl.grid(row=0, column=0, columnspan=2)
output_name = Entry(window, width=20)
output_name.insert(0, 'output')
output_name.grid(row=0, column=2, columnspan=5)
output_btn = Button(window, text="여!", width=10, command=gif_maker)
output_btn.grid(row=0, column=7)

img_lbl = Label(window, text='--image2gif--')
img_lbl.grid(row=1, column=0, columnspan=2)
image_fps_lbl = Label(window, text='fps : ')
image_fps_lbl.grid(row=2, column=0)
image_fps = Combobox(window, values=[0.1, 0.2, 0.5, 0.8, 1.0, 2.0], width=5)
image_fps.current(2)
image_fps.grid(row=2, column=1)
image_scale_lbl = Label(window, text='scale : ')
image_scale_lbl.grid(row=2, column=2)
image_sclae = Combobox(window, values=['max', 'min'], width=10)
image_sclae.current(0)
image_sclae.grid(row=2, column=3, columnspan=3)
img_btn = Button(window, text='Open Images', width=10, anchor="w", command=image_opener)
img_btn.grid(row=2, column=7)

vid_lbl = Label(window, text='--video2gif--')
vid_lbl.grid(row=3, column=0, columnspan=2)
vid_fps_lbl = Label(window, text='fps : ')
vid_fps_lbl.grid(row=4, column=0)
vid_fps = Combobox(window, values=['fps', 20, 12, 10, 6, 5, 3], width=5)
vid_fps.current(0)
vid_fps.grid(row=4, column=1)
vid_btw_label = Label(window, text='section : ')
vid_btw_label.grid(row=4, column=2)
vid_btw_str = Entry(window, width=5)
vid_btw_str.grid(row=4, column=3)
vid_btw_ = Label(window, text='~')
vid_btw_.grid(row=4, column=4)
vid_btw_stp = Entry(window, width=5)
vid_btw_stp.grid(row=4, column=5)
vid_btw_unit = Label(window, text='[sec]')
vid_btw_unit.grid(row=5, column=5)
vid_btn = Button(window, text='Open Video', width=10, anchor="w", command=video_opener)
vid_btw_str.insert(0, 0)
vid_btw_stp.insert(0, 10)
vid_btn.grid(row=4, column=7)


scrolled_list = Label(window, text="List")
scrolled_list.grid(row=5, column=0)
scrolled = scrolledtext.ScrolledText(window, width=45, height=8)
scrolled.grid(row=6, column=0, columnspan=8)


window.mainloop()

print('program done.')