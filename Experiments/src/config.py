import os

BATCH_SIZE = 1
IMG_SIZE = (256, 256, 3)

ROOT_PATH = os.path.abspath(os.path.join(__file__, *((os.path.pardir,)*2)))

DATA_PATH = os.path.join(ROOT_PATH, 'data')

ISLES18_PATH = os.path.join(DATA_PATH, 'isles18')
ISLES18_TRAIN_PATH = os.path.join(ISLES18_PATH, 'train')
ISLES18_TEST_PATH = os.path.join(ISLES18_PATH, 'test')

print("[INFO] Root of codebase at: {}".format(ROOT_PATH))