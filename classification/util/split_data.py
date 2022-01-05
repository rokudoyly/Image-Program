import os
from shutil import copy
import random

# Split dataset. It will create new folder to save the dataset.
def mkfile(file):
    if not os.path.exists(file):
        os.makedirs(file)


file = 'E:/pythonhmk/proj/iclr/picture/train'
class_item = [cla for cla in os.listdir(file) if ".txt" not in cla]
mkfile('E:/pythonhmk/proj/iclr/picture/train/train')

for cla in class_item:
    mkfile('E:/pythonhmk/proj/iclr/picture/train/train/'+cla)

mkfile('E:/pythonhmk/proj/iclr/picture/train/val')
for cla in class_item:
    mkfile('E:/pythonhmk/proj/iclr/picture/train/val/'+cla)

mkfile('E:/pythonhmk/proj/iclr/picture/train/test')
for cla in class_item:
    mkfile('E:/pythonhmk/proj/iclr/picture/train/test/'+cla)

split_rate = 0.2
test_rate = 0.2
for cla in class_item:
    cla_path = file + '/' + cla + '/'
    images = os.listdir(cla_path)
    num = len(images)

    test_index = random.sample(images, k=int(num*test_rate))
    eval_index_old = random.sample(images, k=int(num * split_rate))
    eval_index = [i for i in eval_index_old if i not in test_index]
    for index, image in enumerate(images):
        if image in eval_index:
            image_path = cla_path + image
            new_path = 'E:/pythonhmk/proj/iclr/picture/train/val/' + cla
            copy(image_path, new_path)
        elif image in test_index:
            image_path = cla_path + image
            new_path = 'E:/pythonhmk/proj/iclr/picture/train/test/' + cla
            copy(image_path, new_path)
        else:
            image_path = cla_path + image
            new_path = 'E:/pythonhmk/proj/iclr/picture/train/train/' + cla
            copy(image_path, new_path)
        print("\r[{}] processing [{}/{}]".format(cla, index+1, num), end="")  # processing bar
    print()

print("processing done!")
