from musicpy.musicpy import *
import numpy as np
import os
from tensorflow.keras import layers, Input
from tensorflow.keras.models import Model
from tensorflow.keras.utils import to_categorical

dir = 'B:\\musicproject\\MIDI库\\melody\\'

# dir = 'C:\\music_dev\\proj\\202109\\'
# bpm, a, start_time = read(dir + '1.mid')
# print(a)
# write(a, bpm,  name=dir + '1_out.mid')
# notes = []
# d_n_i = []

len_pool = 4

list_input_n, list_input_di, list_output_n, list_output_di = [], [], [], []
for filenames in os.walk(dir):
    for filename in filenames[2]:
        if filename.endswith('.mid'):
            a = read(os.path.join(dir, filename))[1]
            list_input_n_, list_output_n_, list_input_di_, list_output_di_ = [], [], [], []
            for i in range(1, len(a) - len_pool + 1):
                b = a[i:i + len_pool + 1]
                list_input_n_.append([i.degree for i in b[:-2]])
                list_output_n_.append([b[-1].degree])
                lst1 = [(i.duration if i.duration <= 2 else 2) for i, interval in zip(b, b.interval)]
                lst2 = [(interval if interval <= 2 else 2) for i, interval in zip(b, b.interval)]
                list_input_di_.append(lst1[:-2] + lst2[:-2])
                list_output_di_.append([lst1[-1], lst2[-1]])
            list_input_n.extend(list_input_n_)
            list_output_n.extend(list_output_n_)
            list_input_di.extend(list_input_di_)
            list_output_di.extend(list_output_di_)

input_n = np.array(list_input_n, dtype='uint8')
output_n = to_categorical(np.array(list_output_n, dtype='uint8'), 128)
input_di = np.array(list_input_di, dtype='float32')
output_di = np.array(list_output_di, dtype='float32')

print(input_n.shape, input_di.shape, output_n.shape, output_di.shape)


def build_model():
    notes_input = Input(shape=(len_pool - 1, ), dtype='uint8', name='notes')
    emb = layers.Embedding(128, 64) (notes_input)
    layer1 = layers.LSTM(4) (emb)
    di_input = Input(shape=((len_pool - 1) * 2, ), dtype='float32', name='di')
    layer2 = layers.Dense(512)(di_input)
    concatenated = layers.concatenate([layer1, layer2], axis=-1)
    layer5 = layers.Dense(256)(concatenated)
    layer3 = layers.Dense(128, activation='softmax', name='OutputNote') (layer5)
    layer4 = layers.Dense(2, activation='relu', name='OutputDI') (layer5)

    model = Model([notes_input, di_input], [layer3, layer4])
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['acc'])
    return model


test_train_ratio = 0.9
n_train = int(input_n.shape[0] * test_train_ratio)
print(n_train, input_n.shape[0] - n_train)

input1_train, input1_test, input2_train, input2_test = input_n[:n_train], input_n[n_train:]\
    , input_di[:n_train], input_di[n_train:]
output1_train, output1_test, output2_train, output2_test = output_n[:n_train], output_n[n_train:]\
    , output_di[:n_train], output_di[n_train:]

print()
print(input1_train.shape, input1_test.shape, input2_train.shape, input2_test.shape)
print(output1_train.shape, output1_test.shape, output2_train.shape, output2_test.shape)

model = build_model()

model.fit([input1_train, input2_train], [output1_train, output2_train]
          , validation_data=([input1_test, input2_test], [output1_test, output2_test]), epochs=25, batch_size=4)


