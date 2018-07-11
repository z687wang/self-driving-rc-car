import numpy as np
import cv2

directory = 'training_data'
filename = '1531057753'

data = np.load(directory+"/"+filename+'.npz')

for img in data['train']:
    print(img)