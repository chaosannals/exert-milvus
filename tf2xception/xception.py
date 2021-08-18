from numpy import zeros, expand_dims, linalg
from tensorflow.keras.applications.xception import Xception, preprocess_input
from tensorflow.keras.preprocessing import image


class XceptionExtractor:
    '''
    
    '''

    def __init__(self):
        '''
        '''

        self.input_shape = (299, 299, 3)
        self.model = Xception(
            weights='imagenet',
            input_shape=self.input_shape,
            pooling='avg',
            include_top=False,
        )
        self.model.predict(zeros((1, 299, 299, 3)))

    def extract(self, img_path):
        '''
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