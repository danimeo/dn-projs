from tensorflow.keras import Input, backend
from tensorflow.keras.layers import Dense, Flatten, MaxPooling2D, Conv2D
from tensorflow.keras.models import Model
import numpy as np
import os


'''def build_model():
    x = Input(shape=(36204, ), dtype='float32', name='input')
    # h = Conv1D(32, 7, activation='relu')(x)
    h = Dense(1024, activation='relu')(x)
    h = Dense(512, activation='relu')(h)
    h = Dense(256, activation='relu')(h)
    h = Flatten()(h)
    h = Dense(3 * 32, activation='relu')(h)
    y = Dense(3 * 32, activation='softmax', name='output')(h)
    modl = Model(inputs=x, outputs=y)
    modl.compile(optimizer='adam', loss='mse', metrics=['accuracy'])
    return modl'''


def build_model():
    _input = Input(shape=(84, 173, 1), dtype='float32', name='Input')
    layer1 = Conv2D(16, (2, 2), activation='relu')(_input)
    layer2 = MaxPooling2D(pool_size=(2, 2))(layer1)
    '''layer2 = Conv2D(64, (2, 2), activation='relu')(layer2)
    layer2 = MaxPooling2D(pool_size=(2, 2))(layer2)'''
    layer3 = Flatten()(layer2)

    layer4 = Dense(32 * 128, activation='relu')(layer3)
    # layer4_1 = Dense(32 * 160, activation='relu')(layer4)
    layer4_2 = Dense(32 * 128, activation='softmax', name='n')(layer4)

    layer5 = Dense(32 * 64, activation='relu')(layer3)
    # layer5_1 = Dense(32 * 32, activation='relu')(layer5)
    layer5_2 = Dense(32 * 32, activation='softmax', name='d')(layer5)

    layer6 = Dense(32 * 32, activation='relu')(layer3)
    # layer6_1 = Dense(32 * 32, activation='relu')(layer6)
    layer6_2 = Dense(32 * 1, activation='relu', name='t')(layer6)

    modl = Model([_input], [layer4_2, layer5_2, layer6_2])
    modl.compile(optimizer='adam', loss=['sparse_categorical_crossentropy', 'sparse_categorical_crossentropy', 'mse']
                 , metrics=['acc'])
    return modl


test_train_ratio = 0.8

data_gen_dir = 'data_gen'
input_ = np.load(os.path.join(data_gen_dir, 'input_data.npy'))
output_n = np.load(os.path.join(data_gen_dir, 'output_n_data.npy'))
output_d = np.load(os.path.join(data_gen_dir, 'output_d_data.npy'))
output_t = np.load(os.path.join(data_gen_dir, 'output_t_data.npy'))

n_train = int(input_.shape[0] * test_train_ratio)
print(n_train, input_.shape[0] - n_train)
input_train, input_test = input_[:n_train], input_[n_train:]
output_n_train, output_n_test = output_n[:n_train], output_n[n_train:]
output_d_train, output_d_test = output_d[:n_train], output_d[n_train:]
output_t_train, output_t_test = output_t[:n_train], output_t[n_train:]

print()
print(input_train.shape, input_test.shape)
print(output_n_train.shape, output_n_test.shape)
print(output_d_train.shape, output_d_test.shape)
print(output_t_train.shape, output_t_test.shape)

model = build_model()

inp = input('按回车键开始训练！')

model.fit(x=[input_train], y=[output_n_train, output_d_train, output_t_train]
          , validation_data=(input_test, [output_n_test, output_d_test, output_t_test]), epochs=5, batch_size=4)

backend.clear_session()

print('训练完成。')
