from tensorflow import keras
import numpy as np

model = keras.models.load_model('src/model/neural_network.h5')

def model_predict(X):
    predicted = model.predict(X)
    predicted = predicted[0]
    if predicted[0] > predicted[1]:
        result = {
            'sentiment': 'negative',
            'confidence': np.float64(predicted[0])
        }
    else:
        result = {
            'sentiment': 'positive',
            'confidence': np.float64(predicted[1])
        }
    return result
