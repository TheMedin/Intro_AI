import glob
import pickle
import numpy as np
from PIL import Image

filelist = glob.glob('outputimages/*.bmp')
images = []
for fname in filelist:
    images.append(np.array(Image.open(fname)))
x=np.array(images, "int16")
labels = []
for fname in filelist:
    labels.append(fname[20])
y=np.array(labels)
set = [x, y]
pickle.dump(set, open('handdetectiondataset.pkl', 'wb'), protocol=2)
