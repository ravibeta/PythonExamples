
from Model import ObjectLocalizer
from PIL import Image , ImageDraw
import numpy as np

input_dim = 228

X = np.load( 'processed_data/x.npy')
Y = np.load( 'processed_data/y.npy')
test_X = np.load( 'processed_data/test_x.npy')
test_Y = np.load( 'processed_data/test_y.npy')

print( X.shape )
print( Y.shape )
print( test_X.shape )
print( test_Y.shape )

localizer = ObjectLocalizer( input_shape=( input_dim , input_dim , 3 ) )
#localizer.load_model( 'models/model.h5')
parameters = {
    'batch_size' : 100 ,
    'epochs' : 10 ,
    'callbacks' : None ,
    'val_data' : ( test_X , test_Y )
}

localizer.fit( X , Y  , hyperparameters=parameters )
localizer.save_model( 'models/model.h5')
