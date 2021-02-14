from keras.models import load_model
import nibabel as nib
import numpy as np


model = load_model("model/THE_BEST_RESULT__3 (4).h5")


def testFiles(paths):
    predictions = []
    for i, file_path in enumerate(paths):
        data = []
        
        img = nib.load(file_path)
        img = img.get_fdata() / 2048
        new_img = []
      
        for x, first_l in enumerate(img):
            if x % 4 == 0:
                new_img.append([])
                for j, second_l in enumerate(first_l):
                    if j % 4 == 0:
                        new_img[-1].append(second_l)
        new_img = np.array([new_img], dtype="float")
        data.append(new_img)
        
        for i, d in enumerate(data):
            data[i] = np.resize(d, (128, 128, 32, 1))
        data = np.array(data, dtype="float")
          
        pred = model.predict([[data]])
        if pred[0][0] >= pred[0][1]:
            predictions.append((0, *pred[0]))
        else:
            predictions.append((1, *pred[0]))
    return predictions
