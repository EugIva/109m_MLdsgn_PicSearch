import glob
import os

import cv2
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image as keras_image
import numpy as np


class ImageData:
    def __init__(self, image_path, labels=None):
        self.image_path = image_path
        self.labels = labels if labels is not None else []

    def __contains__(self, item):
        return item in self.labels

    def __str__(self):
        str = ''
        for label in self.labels:
            str += label + ' '
        return f'{os.path.basename(self.image_path)} {str}'


def getLabelOnImage(image_path, model) -> list:
    image = cv2.imread(image_path)
    resized_image = cv2.resize(image, (224, 224))
    resized_image = keras_image.img_to_array(resized_image)
    resized_image = np.expand_dims(resized_image, axis=0)
    resized_image = preprocess_input(resized_image)
    predictions = model.predict(resized_image)
    decoded_predictions = decode_predictions(predictions)

    labels = []

    for i, (imagenet_id, label, score) in enumerate(decoded_predictions[0]):
        labels.append(label)

    return labels


def getLabelsOnDirectory(folder_path) -> (list, list):
    pattern = os.path.join(folder_path, '*.*')
    all_files = glob.glob(pattern)
    image_formats = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    listImages = []
    allLabels = []
    model = MobileNetV2(weights='imagenet')
    for file_path in all_files:
        _, file_extension = os.path.splitext(file_path)
        if file_extension.lower() in image_formats:
            label = getLabelOnImage(file_path, model)
            listImages.append(ImageData(file_path, label))
            for item in label:
                if item not in allLabels:
                    allLabels.append(item)
    print('Все метки, которые удалось найти на изображениях')
    for label in allLabels:
        print(label)

    return allLabels, listImages

def main():
    pass


if __name__ == '__main__':
    main()
