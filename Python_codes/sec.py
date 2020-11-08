import os
import matplotlib.pyplot as plt
import SimpleITK
import pandas as pd
import numpy as np
import math
from skimage.measure import label, regionprops, regionprops_table
from skimage.transform import rotate
from skimage import io
from scipy import ndimage
# Set numpy to print only 2 decimal digits for neatness
np.set_printoptions(precision=2, suppress=True)
import os
import nibabel as nib
from dipy.segment.tissue import TissueClassifierHMRF
from PIL import Image


data_path='/home/sara/Desktop'


example_ni1 = os.path.join(data_path, '009_img.nii.gz')
n1_img = nib.load(example_ni1)
n1_header = n1_img.header

print(n1_header)

n1_img_data = n1_img.get_fdata()
print('Number of rodajas: ',n1_img_data.shape)


def show_slices(slices):
   """ Function to display row of image slices """
   #here we create a plot with n numbers of subplots or images inside, el numero de imagenes dependerá del numero de rodajas que le metas a la Function
   fig, axes = plt.subplots(1, len(slices))

   for i, slice in enumerate(slices):
       axes[i].imshow(slice.T, cmap="gray", origin="lower")

idxSlice = 50


slice_0 = n1_img_data[idxSlice, :, :]
slice_1 = n1_img_data[:, idxSlice, :]
slice_2 = n1_img_data[:, :, idxSlice]


show_slices([slice_0, slice_1, slice_2])
#plt.show()
# Paths to the .mhd files
filenameT1 = "/home/sara/Desktop/pyezzi/fetal_segmentations/010_seg.nii.gz"

# Slice index to visualize with 'sitk_show'

def sitk_show(img, title=None, margin=0.05, dpi=40 ):
    nda = SimpleITK.GetArrayFromImage(img)
    spacing = img.GetSpacing()
    figsize = (1 + margin) * nda.shape[0] / dpi, (1 + margin) * nda.shape[1] / dpi
    extent = (0, nda.shape[1]*spacing[1], nda.shape[0]*spacing[0], 0)
    fig = plt.figure(figsize=figsize, dpi=dpi)
    ax = fig.add_axes([margin, margin, 1 - 2*margin, 1 - 2*margin])

    plt.set_cmap("gray")
    ax.imshow(nda,extent=extent,interpolation=None)

    if title:
        plt.title(title)

    plt.show()
# int label to assign to the segmented gray matter
labelWhiteMatter = 1
labelGrayMatter = 2
imgT1Original = SimpleITK.ReadImage(filenameT1)


imgT1Smooth = SimpleITK.CurvatureFlow(image1=imgT1Original,
                                      timeStep=0.125,
                                      numberOfIterations=5)
imgT1Smooth= SimpleITK.RescaleIntensity(imgT1Smooth)


sitk_show(SimpleITK.Tile(imgT1Smooth[:, :, idxSlice]))

#sitk_show(SimpleITK.Tile(imgT1Smooth[:, :, idxSlice]))


lstSeeds = [(50, 70, idxSlice),
            (105, 120, idxSlice),
            (100, 95, idxSlice),
            (96, 54, idxSlice),
            (95, 54, idxSlice),
            (60, 100, idxSlice)]

imgSeeds = SimpleITK.Image(imgT1Smooth)


for s in lstSeeds:
    print(s)
    imgSeeds[s] = 1000

#sitk_show(imgSeeds[:, :, idxSlice])

imgGrayMatterT1 = SimpleITK.ConfidenceConnected(image1=imgT1Smooth,
                                                seedList=lstSeeds,
                                                numberOfIterations=30,
                                                multiplier=1.167,
                                                replaceValue=labelGrayMatter)

imgT1SmoothInt = SimpleITK.Cast(SimpleITK.RescaleIntensity(imgT1Smooth),
                                imgGrayMatterT1.GetPixelID())
imgGrayMatterT1  = SimpleITK.VotingBinaryHoleFilling(image1=imgGrayMatterT1,
                                                         radius=[2]*3,
                                                         majorityThreshold=1,
                                                         backgroundValue=0,
                                                         foregroundValue=labelGrayMatter)

def sitk_tile_vec(lstImgs):
    lstImgToCompose = []
    for idxComp in range(lstImgs[0].GetNumberOfComponentsPerPixel()):
        lstImgToTile = []
        for img in lstImgs:
            lstImgToTile.append(SimpleITK.VectorIndexSelectionCast(img, idxComp))
        lstImgToCompose.append(SimpleITK.Tile(lstImgToTile, (len(lstImgs), 1, 0)))
    sitk_show(SimpleITK.Compose(lstImgToCompose))


sitk_tile_vec([SimpleITK.LabelOverlay(imgT1SmoothInt[:,:,idxSlice],
                                      imgGrayMatterT1[:,:,idxSlice])])

sitk_show(imgGrayMatterT1[:,:,idxSlice])

shape_stats = SimpleITK.LabelShapeStatisticsImageFilter()



for i in shape_stats.GetLabels():
      print("Label: {0} -> Size (mm): {1} BB(mm): {2}".format(i,shape_stats.GetPhysicalSize(i),shape_stats.GetOrientedBoundingBoxSize(i)))

mask = imgGrayMatterT1[:,:,idxSlice]


image = SimpleITK.GetArrayFromImage(mask)
print(type(image))
label_img = label(image)
regions = regionprops(label_img)


props = regionprops_table(label_img, properties=('centroid',
                                                 'area',
                                                 'perimeter'))

def getLargestCC(segmentation):
    labels = label(segmentation)
    assert( labels.max() != 0 ) # assume at least 1 CC
    largestCC = labels == np.argmax(np.bincount(labels.flat)[1:])+1
    return largestCC

image=getLargestCC(image)
io.imshow(image)
plt.show()
print(pd.DataFrame(props))


from pyezzi import compute_thickness
