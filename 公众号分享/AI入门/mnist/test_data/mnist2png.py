#! /usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：pycharm_ws 
@File    ：mnist2png.py
@IDE     ：PyCharm 
@Author  ：Huajie Sun
@Date    ：2023/7/19 上午11:40
@anno    ：This is a file about 将mnist转为png
'''

from PIL import Image
import idx2numpy
import matplotlib.pyplot as plt

imagefile = '../data/mnist/MNIST/raw/t10k-images-idx3-ubyte'
imagearray = idx2numpy.convert_from_file(imagefile)
print(len(imagearray))

save = None
for i in range(len(imagearray)):
    plt.imshow(imagearray[i], cmap=plt.cm.binary)
    plt.show()

    save = input("save this image(y/n): ")
    if save == "y":
        Image.fromarray(imagearray[i]).save("test_image.png")
        break