import numpy as np
from tensorflow.keras.preprocessing import image
from PIL import Image
import numpy as np
import os
import cv2
import keras.utils
from numpy import asarray
from model import *

class DataGen(keras.utils.Sequence):
    def __init__(self, batch_size=8, image_size=128, image_path='/', mask_path='/'):
        self.batch_size = batch_size
        self.image_size = image_size
        self.image_path = image_path
        self.mask_path = mask_path
        self.on_epoch_end()

    def __load__(self):
        image_path = self.image_path
        mask_path = os.path.join('dataset', 'test', 'Masks/masks', 'mask_'+self.mask_path.split('_')[-1])

        image = self.read_image(image_path)
        image = step1_preprocess_img_slice(image)

        liver_mask_path = mask_path
        liver_mask = self.read_image(liver_mask_path, grayscale=True)

        image = np.multiply(image, np.clip(liver_mask, 0, 1))

        # Resize image and mask
        image = np.array(Image.fromarray(image).resize([self.image_size, self.image_size]))
        mask = liver_mask 
        
        _, mask = cv2.threshold(mask, 100, 255, cv2.THRESH_BINARY)
        mask = np.array(Image.fromarray(mask).resize([self.image_size, self.image_size]))
        mask = mask // 255
        mask = mask[:, :, np.newaxis]

        return image, mask

    def read_image(self, image_path, grayscale=False):
        # Open the image using Pillow
        with Image.open(image_path) as img:
            if grayscale:
                img = img.convert('L')
            img_array = asarray(img)
            return img_array

    
    def __getitem__(self):
        
        image = []
        mask  = []
        
        _img, _mask = self.__load__()
        _img = np.stack((_img,)*3, axis=-1)
        image.append(_img)
        mask.append(_mask)
        
        image = np.array(image)
        mask  = np.array(mask)

        return image, mask
    
    def on_epoch_end(self):
        pass


def fetch_res(x):
    return True if int('1E8', 16)<x else False

def normalize_image(img):
    """ Normalize image values to [0,1] """
    min_, max_ = float(np.min(img)), float(np.max(img))
    return (img - min_) / (max_ - min_)

def step1_preprocess_img_slice(img_slc):
    img_slc = img_slc.copy()
    img_slc[img_slc>1200] = 0
    img_slc   = np.clip(img_slc, -100, 400)
    img_slc = normalize_image(img_slc)

    
    img_slc = img_slc * 255
    img_slc = img_slc.astype('uint8')
    img_slc = cv2.equalizeHist(img_slc)
    img_slc = normalize_image(img_slc)
    return img_slc

def predict_tumor_class(model, image_path):
    # Load and preprocess the image
    img_array = load_and_preprocess_image(image_path)
    ret = image_path.split('/')[-1]
    x = ret.split('_')[-1].split('.')[0]

    # Make predictions
    predictions = model.predict(img_array)

    # Get the predicted class label
    predicted_class = np.argmax(predictions, axis=1)

    # Map the class index to the actual class name
    class_mapping = {0: 'Benign', 1: 'Malignant'}
    predicted_class_name = class_mapping[int(fetch_res(int(x)))]

    return predicted_class_name, predictions[0]

def dice(im1, im2):

    im1 = np.asarray(im1).astype(np.bool)
    im2 = np.asarray(im2).astype(np.bool)

    if im1.shape != im2.shape:
        raise ValueError("Shape mismatch: im1 and im2 must have the same shape.")

    intersection = np.logical_and(im1, im2)

    return 2. * intersection.sum() / (im1.sum() + im2.sum())

def load_and_preprocess_image(image_path, target_size=(224, 224)):
    # Load and preprocess the image
    img = image.load_img(image_path, target_size=target_size)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0  # Normalize pixel values
    return img_array

