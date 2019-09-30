from __future__ import print_function
import requests
import json
import cv2
import base64
import numpy as np
from PIL import Image
from io import BytesIO
import re, time, base64

addr = 'http://localhost:5001'
Get_Image_Colors_url = addr + '/api/getImageColors'

# prepare headers for http request
content_type = 'image/jpeg'
headers = {'content-type': content_type}

img_file = 'Images/1.jpg'
img_shape = cv2.imread(img_file)
print(img_shape.shape)
h,w,b = img_shape.shape
# encode image as jpeg
img = open(img_file, 'rb').read()
# send http request with image and receive response
response = requests.post(Get_Image_Colors_url, data=img, headers=headers)
# decode response
message = json.loads(response.text)
for i, color in enumerate(message["ImageColors"]):
    print("Top color# " + str(i + 1) + ": " + str(color))

#Draw PolyGOn Points
#Convert json points to numpy array of shape Nx2
#cv2.DrawContour(img,numpypoints)
