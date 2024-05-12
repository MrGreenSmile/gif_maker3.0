import cv2
from PIL import Image

file = "F:/작업용/장난감/gif maker/3.0/source/Kenshi Yonezu - Uma to Shika.mp4"
#file = "F:/작업용/장난감/gif maker/3.0/source/part15-30.mp4"
d_start = 120
d_end = 240


Vcap = cv2.VideoCapture(file)

frame_count = int(Vcap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = round(Vcap.get(cv2.CAP_PROP_FPS))
durate = (d_end/fps - d_start/fps)
print(frame_count)
print(fps)
print(durate)

ret, frame = Vcap.read()
h, w, _ = frame.shape

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
image.save('./output/{}.gif'.format('output11'), save_all=True, append_images=images[1:], loop=0xff, duration=durate)
