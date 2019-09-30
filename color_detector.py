from flask import Flask, request, Response, make_response
import cv2
import numpy as np
import jsonpickle

def get_image_colors(img):
    Z = img.reshape((-1,3))

    # convert to np.float32
    Z = np.float32(Z)
    # define criteria, number of clusters(K) and apply kmeans()
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    K = 8
    ret,label,center=cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
    y = np.bincount(label[:,0])
    ii = np.nonzero(y)[0]
    x_ = (zip(ii,y[ii]))


    x_ = sorted(x_, key=lambda x:x[1], reverse=True)
    # Now convert back into uint8, and make original image
    center = np.uint8(center)
    res = center[label.flatten()]
    res2 = res.reshape((img.shape))

    colors = center
    Colors = []
    for i in range(8):
        try:
            color_pix = [int(colors[x_[i][0]][2]), int(colors[x_[i][0]][1]), int(colors[x_[i][0]][0])]
        except IndexError:
            return []
        Colors.append(color_pix)
    return Colors


app = Flask(__name__)
@app.route('/api/getImageColors', methods=['POST'])
def getImageColors():
    r = request
    nparr = np.fromstring(r.data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    colors = get_image_colors(img)
    response = {'ImageColors': colors}
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)