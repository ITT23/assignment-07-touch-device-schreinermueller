import numpy as np
import os
import time
import config as c
import keras

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from keras.models import Sequential
from keras.layers import Dense, LSTM
from keras.callbacks import ReduceLROnPlateau, EarlyStopping
from keras.utils import to_categorical
from tqdm.notebook import tqdm
from sklearn.model_selection import train_test_split
from scipy.signal import resample
import xml.etree.ElementTree as ET
from sklearn.preprocessing import LabelEncoder, StandardScaler


class UniStroke:
    def __init__(self) -> None:
        
        # data = load_data()
        # X_train, X_test, y_train, y_test, labels, self.encoder = prepare_data(data)
        # self.model_32, self.history_32 = create_model(X_train, X_test, y_train, y_test, labels)
        # self.model_32.save('gesture_recognition')
        self.model_32 = keras.models.load_model("gesture_recognition")
        self.encoder = LabelEncoder()
        labels = c.Gestures.THREE
        labels_encoded = self.encoder.fit_transform(labels)

    def predict_gesture(self, model, encoder, gesture):
        scaler = StandardScaler()
        gesture = scaler.fit_transform(gesture)
        gesture = resample(gesture, c.RecognizerSetup.NUM_POINTS)
        prediction = model.predict(np.array([gesture]))
        print(prediction)
        prediction = np.argmax(prediction)
        prediction_label = encoder.inverse_transform(np.array([prediction]))[0]
        print(prediction_label)
        return prediction_label

def load_data():
    data = []

    for root, subdirs, files in os.walk('dataset'):
        if 'ipynb_checkpoint' in root:
            continue

        if len(files) > 0:
            print("yes")
            for f in tqdm(files):
                if '.xml' in f:
                    fname = f.split('.')[0]
                    label = fname[:-2]
                    if label in c.Gestures.THREE:
                        xml_root = ET.parse(f'{root}/{f}').getroot()

                        points = []
                        for element in xml_root.findall('Point'):
                            x = element.get('X')
                            y = element.get('Y')
                            points.append([x, y])

                        points = np.array(points, dtype=float)

                        scaler = StandardScaler()
                        points = scaler.fit_transform(points)

                        resampled = resample(points, c.RecognizerSetup.NUM_POINTS)

                        data.append((label, resampled))
    print(data[:3])
    return data


def prepare_data(data):
    labels = [sample[0] for sample in data]
    print(set(labels))

    encoder = LabelEncoder()
    labels_encoded = encoder.fit_transform(labels)

    print(set(labels_encoded))
    y = to_categorical(labels_encoded)
    print(len(y[0]))

    sequences = [sample[1] for sample in data]
    X = np.array(sequences)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)
    
    return X_train, X_test, y_train, y_test, labels, encoder


def create_model(X_train, X_test, y_train, y_test, labels):
    model = Sequential()
    model.add(LSTM(32, input_shape=(c.RecognizerSetup.NUM_POINTS, 2)))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(len(set(labels)), activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=2, min_lr=0.0001)
    stop_early = EarlyStopping(monitor='val_loss', patience=3)
    
    history = model.fit(
        X_train,
        y_train,
        epochs=20,
        batch_size=32,
        validation_data=(X_test, y_test),
        verbose=1,
        callbacks=[reduce_lr, stop_early]
    )
    
    model.summary()
    
    return model, history


def predict_gesture(model, encoder, gesture):
    prediction = model.predict(np.array([gesture]))
    prediction = np.argmax(prediction)
    prediction_label = encoder.inverse_transform(np.array([prediction]))[0]
    print(prediction_label)

