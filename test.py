import os

filename = "./data/006544d878c4b413d77d3e8d8c2b2e1d"
#os.rename(filename, filename + ".nii.gz")
filename += ".nii.gz"

from nibabel.testing import data_path
example_filename = os.path.join(filename)

import nibabel as nib
img = nib.load(example_filename)

array = img.get_fdata()

from PIL import Image, ImageDraw
image = Image.new("RGB", (512, 512), (0, 0, 0))
for x in range(512):
    for y in range(512):
        value = (array[x][y][0] + 2048) // 16
        value = int(min(255, value))
        image.putpixel((x, y), (value, value, value))
image.save("data/image1.png", "PNG")