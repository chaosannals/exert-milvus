from numpy import zeros, expand_dims, linalg
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.preprocessing import image

class VGG16Extractor:
    '''
    特征提取器。
    '''

    def __init__(self):
        '''
        初始化。
        '''
        self.input_shape = (224, 224, 3)
        self.model = VGG16(
            weights='imagenet',
            input_shape=self.input_shape,
            pooling='max',
            include_top=False
        )
        self.model.predict(zeros((1, 224, 224, 3)))

    def extract(self, img_path):
        '''
        提取特征向量。
        '''
        img = image.load_img(
            img_path,
            target_size=(
                self.input_shape[0],
                self.input_shape[1]
            )
        )
        img = image.img_to_array(img)
        img = expand_dims(img, axis=0)
        img = preprocess_input(img)
        feat = self.model.predict(img)
        norm_feat = feat[0] / linalg.norm(feat[0])
        return [i.item() for i in norm_feat]
