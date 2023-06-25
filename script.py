import cv2
import os
import numpy as np

def get_images():
    path = 'TestImages'
    Images =[]
    ImgList = os.listdir(path)

    for img in ImgList:
        print(f"{path}/{img}")
        curImg = cv2.imread(f'{path}/{img}')
        Images.append(curImg)

    return Images,ImgList

class Preprocessing:

    def __init__(self, img) -> None:
        self.img = img
        cv2.imshow("Original Image", self.img)
        cv2.waitKey(500)

    def contrast_enhancement(self):
        alpha = 1.5
        beta = 0
        self.cont_enh_img = cv2.convertScaleAbs(self.img, alpha=alpha, beta = beta)
        cv2.imshow('Contrast Enhanced', self.cont_enh_img)
        cv2.waitKey(500)

    def color_enhancement(self):
        self.img = self.cont_enh_img
        hsv = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        s = cv2.add(s, 50)
        v = cv2.add(v, 50)
        enhanced_hsv = cv2.merge([h, s, v])
        self.color_enhanced_img = cv2.cvtColor(enhanced_hsv, cv2.COLOR_HSV2BGR)
        cv2.imshow('Color Enhanced', self.color_enhanced_img)
        cv2.waitKey(500)

    def noise_reduction(self):
        self.img = self.color_enhanced_img
        kernel_size = 3
        self.denoised_img = cv2.GaussianBlur(self.img, (kernel_size, kernel_size), 0)
        cv2.imshow('Noise Reduced', self.denoised_img)
        cv2.waitKey(500)

    def edge_enhancement(self):
        self.img = self.denoised_img
        kernel_size = 5
        sigma = 1
        lab_img = cv2.cvtColor(self.img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab_img)
        # blurred_l = cv2.GaussianBlur(l, (kernel_size, kernel_size), sigma)
        sharpened_l = cv2.addWeighted(l, 1.5, l, -0.5, 0)
        lab_img = cv2.merge([sharpened_l, a, b])
        self.sharpened_img = cv2.cvtColor(lab_img, cv2.COLOR_LAB2BGR)
        cv2.imshow('Edge Enhanced', self.sharpened_img)
        cv2.waitKey(500)

def main():

    Images, ImgList = get_images()
    outputImgs = []

    for img in Images:
        P1 = Preprocessing(img)
        P1.contrast_enhancement()
        P1.color_enhancement()
        P1.noise_reduction()
        P1.edge_enhancement()
        cv2.destroyAllWindows()
        outputImgs.append([img, P1.cont_enh_img, P1.color_enhanced_img, P1.denoised_img, P1.sharpened_img])

    resized_images = []
    for img in Images:
        resized_images.append(cv2.resize(img, (300, 225)))

    resized_output_images = []
    for i, imgData in enumerate(outputImgs):
        resized_output_images.append([cv2.resize(img, (300, 225)) for img in imgData])

    for i, imgData in enumerate(resized_output_images):
        imgStack = np.hstack(imgData)
        cv2.imshow(f'IMG {i}', imgStack)
        cv2.waitKey(0)

if __name__ == "__main__":
    main()
