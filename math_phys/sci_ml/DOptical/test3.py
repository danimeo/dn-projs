import scipy.io as sio
import numpy as np
import torch
from torch import nn
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
from torch.autograd import Variable
import math
import csv
    
from raytracing import *
 
# Define LSTM Neural Networks
class GruRNN(nn.Module):
    """
        Parameters：
        - input_size: feature size
        - hidden_size: number of hidden units
        - output_size: number of output
        - num_layers: layers of LSTM to stack
    """
 
    def __init__(self, input_size, hidden_size=1, output_size=1, num_layers=1):
        super().__init__()
 
        self.lstm = nn.GRU(input_size, hidden_size, num_layers)  # utilize the GRU model in torch.nn
        self.linear1 = nn.Linear(hidden_size, 16) # 全连接层
        self.linear2 = nn.Linear(16, output_size) # 全连接层
 
    def forward(self, _x):
        x, _ = self.gru(_x)  # _x is input, size (seq_len, batch, input_size)
        s, b, h = x.shape  # x is output, size (seq_len, batch, hidden_size)
        x = x.view(s * b, h)
        x = self.linear1(x)
        x = self.linear2(x)
        x = x.view(s, b, -1)
        return x
 
if __name__ == '__main__':

    path = ImagingPath()
    path.append(Space(d=50))
    path.append(Lens(f=50, diameter=25))
    path.append(Space(d=120))
    path.append(Lens(f=70))
    path.append(Space(d=100))
    path.display()
 
    # checking if GPU is available
    device = torch.device("cpu")
 
    if (torch.cuda.is_available()):
        device = torch.device("cuda:0")
        print('Training on GPU.')
    else:
        print('No GPU available, training on CPU.')
 
    # 数据读取&类型转换
    data_x = np.array(pd.read_csv('Data_x.csv', header=None)).astype('float32')
    data_y = np.array(pd.read_csv('Data_y.csv', header=None)).astype('float32')
 
    # 数据集分割
    data_len = len(data_x)
    t = np.linspace(0, data_len, data_len + 1)
 
    train_data_ratio = 0.8  # Choose 80% of the data for training
    train_data_len = int(data_len * train_data_ratio)
 
    train_x = data_x[5:train_data_len]
    train_y = data_y[5:train_data_len]
    t_for_training = t[5:train_data_len]
 
    test_x = data_x[train_data_len:]
    test_y = data_y[train_data_len:]
    t_for_testing = t[train_data_len:]
 
    # ----------------- train -------------------
    INPUT_FEATURES_NUM = 5
    OUTPUT_FEATURES_NUM = 1
    train_x_tensor = train_x.reshape(-1, 1, INPUT_FEATURES_NUM)  # set batch size to 1
    train_y_tensor = train_y.reshape(-1, 1, OUTPUT_FEATURES_NUM)  # set batch size to 1
 
    # transfer data to pytorch tensor
    train_x_tensor = torch.from_numpy(train_x_tensor)
    train_y_tensor = torch.from_numpy(train_y_tensor)
 
    gru_model = GruRNN(INPUT_FEATURES_NUM, 30, output_size=OUTPUT_FEATURES_NUM, num_layers=1)  # 30 hidden units
    print('GRU model:', gru_model )
    print('model.parameters:', gru_model .parameters)
    print('train x tensor dimension:', Variable(train_x_tensor).size())
 
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(gru_model .parameters(), lr=1e-2)
 
    prev_loss = 1000
    max_epochs = 2000
 
    train_x_tensor = train_x_tensor.to(device)
 
    # for epoch in range(max_epochs):
    #     output = gru_model(train_x_tensor).to(device)
    #     loss = criterion(output, train_y_tensor)
 
    #     optimizer.zero_grad()
    #     loss.backward()
    #     optimizer.step()
 
    #     if loss < prev_loss:
    #         torch.save(gru_model.state_dict(), 'lstm_model.pt')  # save model parameters to files
    #         prev_loss = loss
 
    #     if loss.item() < 1e-4:
    #         print('Epoch [{}/{}], Loss: {:.5f}'.format(epoch + 1, max_epochs, loss.item()))
    #         print("The loss value is reached")
    #         break
    #     elif (epoch + 1) % 100 == 0:
    #         print('Epoch: [{}/{}], Loss:{:.5f}'.format(epoch + 1, max_epochs, loss.item()))
 
    # # prediction on training dataset
    # pred_y_for_train = gru_model(train_x_tensor).to(device)
    # pred_y_for_train = pred_y_for_train.view(-1, OUTPUT_FEATURES_NUM).data.numpy()
 
    # # ----------------- test -------------------
    # gru_model = gru_model .eval()  # switch to testing model
 
    # # prediction on test dataset
    # test_x_tensor = test_x.reshape(-1, 1,
    #                                INPUT_FEATURES_NUM)
    # test_x_tensor = torch.from_numpy(test_x_tensor)  # 变为tensor
    # test_x_tensor = test_x_tensor.to(device)
 
    # pred_y_for_test = gru_model(test_x_tensor).to(device)
    # pred_y_for_test = pred_y_for_test.view(-1, OUTPUT_FEATURES_NUM).data.numpy()
 
    # loss = criterion(torch.from_numpy(pred_y_for_test), torch.from_numpy(test_y))
    # print("test loss：", loss.item())
 
    # # ----------------- plot -------------------
    # plt.figure()
    # plt.plot(t_for_training, train_y, 'b', label='y_trn')
    # plt.plot(t_for_training, pred_y_for_train, 'y--', label='pre_trn')
 
    # plt.plot(t_for_testing, test_y, 'k', label='y_tst')
    # plt.plot(t_for_testing, pred_y_for_test, 'm--', label='pre_tst')
 
    # plt.xlabel('t')
    # plt.ylabel('Vce')
    # plt.show()