import os

HEALTHY_WAY = '/data/healthy'
SICK_WAY = '/data/sick'

for fileway in [HEALTHY_WAY, SICK_WAY]:
    for file in os.listdir(fileway):
        if not file.endswith(".nii.gz"):
            os.rename(fileway + '/' + file,
                      fileway + '/' + file + ".nii.gz")     
