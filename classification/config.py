from easydict import EasyDict as edict

__C = edict()
cfg = __C

#Basic setting
__C.BASIC = edict()
__C.BASIC.WEIGHT = 128
__C.BASIC.HIGHT = 128
__C.BASIC.PATH = './dataset/'
__C.BASIC.SAVEMODEL = False


#PCA
__C.DEMON = edict()
__C.DEMON.PCA = True
__C.DEMON.REDUCE = [400]

