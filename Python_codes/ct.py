import os
import matplotlib.pyplot as plt
import SimpleITK
import pandas as pd
import numpy as np
import math
import sys
from skimage.measure import label, regionprops, regionprops_table
from skimage.transform import rotate
from skimage import io
from scipy import ndimage
from skimage import restoration
from skimage import filters
import cv2
# Set numpy to print only 2 decimal digits for neatness
np.set_printoptions(precision=2, suppress=True)
import os
import nibabel as nib
from dipy.segment.tissue import TissueClassifierHMRF
from PIL import Image
import logging
import numpy as np
from pyezzi import compute_thickness, cropping


def remove_keymap_conflicts(new_keys_set):
    for prop in plt.rcParams:
        if prop.startswith('keymap.'):
            keys = plt.rcParams[prop]
            remove_list = set(keys) & new_keys_set
            for key in remove_list:
                keys.remove(key)

def multi_slice_viewer(volume):
    remove_keymap_conflicts({'j', 'k'})
    fig, ax = plt.subplots()
    ax.volume = volume
    ax.index = volume.shape[0] // 2
    ax.imshow(volume[ax.index])
    fig.canvas.mpl_connect('key_press_event', process_key)


def process_key(event):
    fig = event.canvas.figure
    ax = fig.axes[0]
    if event.key == 'j':
        previous_slice(ax)
    elif event.key == 'k':
        next_slice(ax)
    fig.canvas.draw()

def previous_slice(ax):
    volume = ax.volume
    ax.index = (ax.index - 1) % volume.shape[0]  # wrap around using %
    ax.images[0].set_array(volume[ax.index])

def next_slice(ax):
    volume = ax.volume
    ax.index = (ax.index + 1) % volume.shape[0]
    ax.images[0].set_array(volume[ax.index])

filenameT1 = "/home/sara/Desktop/pyezzi/fetal_segmentations/035_seg.nii.gz"

np.set_printoptions(threshold=sys.maxsize)




labelWhiteMatter = 1
labelGrayMatter = 2
img = SimpleITK.ReadImage(filenameT1)


image = SimpleITK.GetArrayFromImage(img)





print('Values of the colors',np.unique(image))



multi_slice_viewer(image)

print('Shape ',np.shape(image))
print('Dimensions ',np.ndim(image))
print('Size ',np.size(image))



a=np.where(image==2)
image[a]= 8
c=np.where(image==1) #WM DERECHA
image[c]= 0
c=np.where(image==3)
image[c]= 1
c=np.where(image==4)
image[c]= 1
c=np.where(image==5)
image[c]= 0
c=np.where(image==6)
image[c]= 0
c=np.where(image==7)
image[c]= 0
c=np.where(image==9) #WM IZQUIERDA
image[c]= 1
c=np.where(image==10) # VENTRICULO IZQUIERDO
image[c]= 1
c=np.where(image==11)
image[c]= 0
c=np.where(image==12)
image[c]= 0


c=np.where(image==8)
image[c]= 2

#6:cerebelo derecho
#7. liquido cefaloraquideo izquierdo
#8: cortex izquierdo
#2: cortex derecho
cortex=np.where(image==2)
print('Second values of colors  ',np.unique(image))

multi_slice_viewer(image)





for key in img.GetMetaDataKeys():
        print("\"{0}\":\"{1}\"".format(key, img.GetMetaData(key)))





print('Shape ',np.shape(image))
print('Dimensions ',np.ndim(image))
print('Size ',np.size(image))

from skimage import data
from skimage import filters
camera = data.camera()
val = filters.threshold_otsu(camera)
mask = camera < val

thickness = compute_thickness(image)

print('Shape ',np.shape(image))
print('Dimensions ',np.ndim(image))
print('Size ',np.size(image))



print(type(thickness))


thickness_values = np.nan_to_num(thickness[cortex])

print('Dimensions ',np.ndim(thickness[cortex]))
print(type(thickness_values))

print("Resultados (en que unidades?? ) max = {}, mean = {}, min = {}, std = {}".format(thickness_values.max(),
                                                      thickness_values.mean(),
                                                      thickness_values.min(),
                                                      thickness_values.std()))
print("Si tenemos en cuenta que el pixdim (segun itkSnap) es 0.075, pues eñ thickness sería: ",thickness_values.mean()*0.75)



multi_slice_viewer(thickness)

s = 100
f, ax = plt.subplots()
plt.imshow(thickness[s])
plt.colorbar()
plt.show()
