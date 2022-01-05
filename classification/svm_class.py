# -*- coding: utf-8 -*-
import cv2
import logging
import joblib
import numpy as np
from pathlib import Path
from sklearn.utils import Bunch
from sklearn import svm, metrics, datasets
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.decomposition import PCA
from tqdm import tqdm
from config import cfg
from time import time

# Before running code, this file needs to be placed in the same directory as config.py

def load_data(img_path, weight=None, hight=None):
    """ Load image dataset.
        PATH: ./dataset/
    """
    desc = "image classification dataset"
    image_dir = Path(img_path)
    folders = [path for path in image_dir.iterdir() if path.is_dir()]
    categories = [folder.name for folder in folders]
    images = []
    flatt_img = []
    target = []
    num = 0

    for tg, direction in tqdm(enumerate(folders), total=len(folders)):
        for file in direction.iterdir():
            imgpath = img_path + direction.name + '/' + file.name
            img = cv2.imread(imgpath, cv2.IMREAD_UNCHANGED)
            img_resize = cv2.resize(img, (weight, hight))
            flatt_img.append(img_resize.flatten())
            images.append(img_resize)
            target.append(tg)
            num += 1
            logging.info('Loading %s; Success load %d pictures...'%(direction.name, num))
    flatt_img = np.array(flatt_img)
    target = np.array(target)
    images = np.array(images)

    return Bunch(data=flatt_img,
                 target=target,
                 target_names=categories,
                 images=images,
                 DESCR=desc)

def pca(cfg, X_train, X_test, param_grid, y_train, reduce):
    """ PCA part.
    """
    logging.info('Setting PCA %d...' % reduce)
    pca = PCA(n_components=reduce).fit(X_train)
    X_train_pca = pca.transform(X_train)  # 将训练集投影到低维空间
    X_test_pca = pca.transform(X_test)
    svc = svm.SVC()
    clf = GridSearchCV(svc, param_grid)
    clf.fit(X_train_pca, y_train)
    if cfg.BASIC.SAVEMODEL is True:
        joblib.dump(clf, "svm_4class_pca.m")
    logging.info('Successful PCA %d...' % reduce)
    return X_test_pca, clf

def dataset(cfg):
    """ Load Dataset and split.
    """
    image_dataset = load_data(cfg.BASIC.PATH, cfg.BASIC.WEIGHT, cfg.BASIC.HIGHT)
    X_train, X_test, y_train, y_test = train_test_split(
        image_dataset.data, image_dataset.target, test_size=0.2, random_state=100)
    logging.info('Successful split dataset...')
    param_grid = [
        {'C': [1, 10, 100, 1000], 'kernel': ['linear']},
        {'C': [1, 10, 100, 1000], 'gamma': [0.001, 0.0001], 'kernel': ['rbf']},
    ]
    return X_train, X_test, y_train, y_test, param_grid

def model(cfg, X_train, X_test, y_train, param_grid, reduce):
    """ Model part (Use SVM).
    """
    if cfg.DEMON.PCA is True:
        X_test, clf = pca(cfg, X_train, X_test, param_grid, y_train, reduce)
    else:
        logging.info('Start svm...')
        svc = svm.SVC()
        clf = GridSearchCV(svc, param_grid)
        clf.fit(X_train, y_train)
        joblib.dump(clf, "svm_4class_nopca.m")
        logging.info('Finish svm...')
    return X_test, clf

def run(cfg, X_train, X_test, y_train, y_test, param_grid):
    """ Running part.
    """
    record_time = []
    for reduce in list(cfg.DEMON.REDUCE):
        starttime = time()
        #reduce=cfg.DEMON.REDUCE
        X_test_new, clf = model(cfg, X_train, X_test, y_train, param_grid, reduce)
        endtime = time()-starttime
        y_pred = clf.predict(X_test_new)
        endtest = time()-starttime
        alltime = endtest-endtime
        record = '\n'+'Train time:'+ str(endtime)+'\n'+'Test and Train time:'+str(endtest) + 'Test time:'+str(alltime)
        scorename = 'score' + str(reduce) + '.txt'
        score = "Classification report for - \n{}:\n{}\n".format(
            clf, metrics.classification_report(y_test, y_pred))
        with open(scorename,'w',encoding='utf8') as f:
            f.write(str(score))
            f.write(record)
        print("Classification report for - \n{}:\n{}\n".format(
            clf, metrics.classification_report(y_test, y_pred)))
        print(' ')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s: %(message)s')
    X_train, X_test, y_train, y_test, param_grid = dataset(cfg)
    run(cfg, X_train, X_test, y_train, y_test, param_grid)
