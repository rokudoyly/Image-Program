# -*- coding: utf-8 -*-
import os
import cv2
import numpy as np
import random
from tqdm import tqdm
import string
# Data Augmentation
def is_image_file(filename):  #
    return any(filename.endswith(extension) for extension in [".png", ".jpg", ".jpeg", ".tif", ".tiff"])


def is_damaged(cvimage):
    height, weight, channel = cvimage.shape
    one_channel = np.sum(cvimage, axis=2)
    white_pixel_count = len(one_channel[one_channel == 255 * 3])  # Count the number of white pixels
    if white_pixel_count > 0.08 * height * weight:
        return True
    return False


def gamma_transform(img, gamma):
    gamma_table = [np.power(x / 255.0, gamma) * 255.0 for x in range(256)]
    gamma_table = np.round(np.array(gamma_table)).astype(np.uint8)
    return cv2.LUT(img, gamma_table)


def random_gamma_transform(img, gamma_vari):
    log_gamma_vari = np.log(gamma_vari)
    alpha = np.random.uniform(-log_gamma_vari, log_gamma_vari)
    gamma = np.exp(alpha)
    return gamma_transform(img, gamma)


def rotate(xb, yb, angle):
    M_rotate = cv2.getRotationMatrix2D((img_w / 2, img_h / 2), angle, 1)
    xb = cv2.warpAffine(xb, M_rotate, (img_w, img_h))
    if yb is not None:
        yb = cv2.warpAffine(yb, M_rotate, (img_w, img_h))
    return xb, yb


def blur(img):
    img = cv2.blur(img, (3, 3))
    return img


def add_noise(img):
    for i in range(200):
        temp_x = np.random.randint(0, img.shape[0])
        temp_y = np.random.randint(0, img.shape[1])
        img[temp_x][temp_y] = 255
    return img


def data_augment(xb, yb=None, rotate=None):
    if rotate is not None:
        if np.random.random() < 0.25:
            xb, yb = rotate(xb, yb, 90)
        if np.random.random() < 0.25:
            xb, yb = rotate(xb, yb, 180)
        if np.random.random() < 0.25:
            xb, yb = rotate(xb, yb, 270)
    if np.random.random() < 0.25:
        xb = cv2.flip(xb, 1)
        if yb is not None:
            yb = cv2.flip(yb, 1)

    if np.random.random() < 0.25:
        xb = random_gamma_transform(xb, 1.0)

    if np.random.random() < 0.25:
        xb = blur(xb)

    if np.random.random() < 0.25:
        xb = add_noise(xb)

    return xb, yb


def creat_dataset(image_sets, img_w, img_h, image_num=600, mode='augment'):
    print('creating dataset...')
    image_each = image_num / len(image_sets)
    g_count = 0
    for i in tqdm(range(len(image_sets))):
        count = 0
        src_img = cv2.imread('E:/pythonhmk/proj/iclr/picture/rabbit/' + image_sets[i])  # 3 channels
        label = None
        X_height, X_width, _ = src_img.shape
        while count < image_each:
            random_width = random.randint(0, X_width - img_w - 1)
            random_height = random.randint(0, X_height - img_h - 1)
            src_roi = src_img[random_height: random_height + img_h, random_width: random_width + img_w, :]
            #src_roi = src_img
            if is_damaged(src_roi):
                 continue
            if mode == 'augment':
                src_roi, _ = data_augment(src_roi, label, rotate=None)
            name = ''.join(random.sample(string.digits + string.ascii_letters, 6))
            cv2.imwrite(('E:/pythonhmk/proj/iclr/picture/train/rabbit/%s_rabbit.png' % name), src_roi)
            count += 1
            g_count += 1


if __name__ == '__main__':
    img_w = 224
    img_h = 224
    src_data_path = 'E:/pythonhmk/proj/iclr/picture/rabbit'
    image_sets2 = [x for x in os.listdir(src_data_path) if is_image_file(x)]
    creat_dataset(image_sets=image_sets2, img_w=img_w, img_h=img_h)