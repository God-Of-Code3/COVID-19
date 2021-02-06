from imutils import paths
import numpy as np
import random
import pickle
import os

from nibabel.testing import data_path
import nibabel as nib


HEALTHY_WAY = '/data/healthy'
SICK_WAY = '/data/sick'

DATA_WAY = ''
LABELS_WAY = ''

ImagePaths = os.listdir(HEALTHY_WAY) + os.listdir(SICK_WAY)
print('Size of data:', len(ImagePaths))
random.shuffle(ImagePaths)

data = []
labels = []

for file in ImagePaths:
  if file in os.listdir(HEALTHY_WAY):
    img = nib.load(HEALTHY_WAY + '/' + file)
    label = [1, 0]
  else:
    img = nib.load(SICK_WAY + '/' + file)
    label = [0, 1]
  data.append(img.get_fdata())
  labels.append(label)

print('data:', data)
print('labels:', labels)

with open(DATA_WAY + '/' + 'data.pickle', "wb") as f:
  pickle.dump(data, f)
print("Data saved")

with open(LABELS_WAY + '/' + 'labels.pickle', "wb") as f:
  pickle.dump(labels, f)
print("Labels saved")
