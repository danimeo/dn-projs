import random

import numpy as np
import scipy.signal
import torch
import torch.nn.functional
import matplotlib.pyplot as plt
import math

# checking if GPU is available
from scipy.signal import butter

device = torch.device("cpu")

if torch.cuda.is_available():
    device = torch.device("cuda:0")
    print('Training on GPU.')
else:
    print('No GPU available, training on CPU.')


mat0100 = torch.tensor([[0, 1], [0, 0]], dtype=torch.float32).to(device)
mat0010 = torch.tensor([[0, 0], [1, 0]], dtype=torch.float32).to(device)
mat1101 = torch.tensor([[1, 1], [0, 1]], dtype=torch.float32).to(device)
mat1001 = torch.tensor([[1, 0], [0, 1]], dtype=torch.float32).to(device)
one = torch.tensor(1.0, dtype=torch.float32).to(device)

a_r, c_r = torch.tensor(10, dtype=torch.float32).to(device), torch.tensor(190, dtype=torch.float32).to(device)
a_t, c_t = torch.tensor(2, dtype=torch.float32).to(device), torch.tensor(68, dtype=torch.float32).to(device)
b_t_glass = torch.tensor(10, dtype=torch.float32).to(device)


def x2_mat(x, n):
    x2 = torch.ones((x.size(-1), 1)).to(device)
    x_ = torch.unsqueeze(x, dim=-1)
    for i3 in range(1, int(n / 2)):
        # x3 *= torch.reshape(x, (-1, 1))
        x3_1, x3_2 = torch.cos(i3 * x_), torch.sin(i3 * x_)
        # print(x2.size(), x3_1.size())
        x2 = torch.hstack([x2, x3_1, x3_2])
    i3 = 1
    x2 = torch.hstack([x2, torch.cos(i3 * x_)])
    if x2.size(-1) < n:
        i3 = int(n / 2)
        x2 = torch.hstack([x2, torch.sin(i3 * x_)])
    return x2  # torch.clamp(x2, min=-1e3, max=1e3)


class OpticalModel(torch.nn.Module):
    def __init__(self, obj_dist, materials, n_points, img_height):
        super().__init__()
        self.materials = materials
        self.obj_dist = obj_dist
        self.n_surfs = len(materials)
        self.n_points = n_points
        self.img_height = img_height

        self.img_scale = torch.linspace(-img_height, img_height, n_points).to(device)

        self.rath_param = [torch.nn.Parameter(torch.rand(size=(4,)).to(device), requires_grad=True) for _ in range(self.n_surfs)]
        self.p_param = [torch.nn.Parameter(0.5 * torch.ones(size=(4,)).to(device), requires_grad=True) for _ in range(self.n_surfs)]
        # self.rath_param = [torch.nn.Parameter(torch.rand(size=(2, 2)).to(device), requires_grad=True) for _ in range(self.n_surfs)]

        self.obj_unif = torch.tensor([[1, self.obj_dist], [0, 1]], dtype=torch.float32).to(device)

        for i in range(self.n_surfs):
            self.register_parameter('RT' + str(i), self.rath_param[i])
            self.register_parameter('P' + str(i), self.p_param[i])

        self.fc = torch.nn.Sequential(
            torch.nn.Linear(4, 128),
            torch.nn.Dropout(0.01),
            torch.nn.LeakyReLU(),
            torch.nn.Linear(128, 64),
            torch.nn.Dropout(0.01),
            torch.nn.LeakyReLU(),
            torch.nn.Linear(64, 8),
            torch.nn.Dropout(0.01),
            torch.nn.LeakyReLU(),
            torch.nn.Linear(8, 4),
            # torch.nn.Sigmoid(),
        ).to(device)

        self.fc2 = torch.nn.Sequential(
            torch.nn.Linear(4, 128),
            torch.nn.Dropout(0.01),
            torch.nn.LeakyReLU(),
            torch.nn.Linear(128, 64),
            torch.nn.Dropout(0.01),
            torch.nn.LeakyReLU(),
            torch.nn.Linear(64, 8),
            torch.nn.Dropout(0.01),
            torch.nn.LeakyReLU(),
            torch.nn.Linear(8, 4),
            torch.nn.Sigmoid(),
        ).to(device)

        # self.fc_p = torch.nn.Sequential(
        #     torch.nn.Linear(256, 128),
        #     torch.nn.Dropout(0.1),
        #     torch.nn.LeakyReLU(),
        #     torch.nn.Linear(128, 8),
        #     torch.nn.Dropout(0.1),
        #     torch.nn.LeakyReLU(),
        #     torch.nn.Linear(8, 1),
        #     # torch.nn.Sigmoid(),
        # ).to(device)

        self.rath = []
        for i in range(len(self.rath_param)):
            fc2_out = self.p_param[i]
            rath_param = torch.reshape(fc2_out * self.fc2(self.rath_param[i]).to(device) + (1 - fc2_out) * torch.rand_like(self.rath_param[i]).to(device), (2, 2))
            # rath_param = self.rath_param[i]
            self.rath.append(mat1001\
                           + (a_r * torch.sign(rath_param) + c_r * (2 * rath_param - 1)) * mat0010\
                           + (a_t + (c_t * rath_param if i % 2 == 1 else b_t_glass * rath_param)) * mat0100
                             )

    def forward(self, x, obj):
        unisurf = self.obj_unif.clone().to(device)

        for i in range(len(self.rath)):
            fc2_out = self.p_param[i]
            rath_param = torch.reshape(fc2_out * self.fc2(self.rath_param[i]).to(device) + (1 - fc2_out) * torch.rand_like(self.rath_param[i]).to(device), (2, 2))
            # rath_param = self.rath_param[i]
            # self.rath[i] = mat1001 \
            #                + (a_r * torch.sign(2 * rath_param - 1) + c_r * (2 * rath_param - 1)) * mat0010 \
            #                + (a_t + (c_t * rath_param if i % 2 == 1 else b_t_glass * rath_param)) * mat0100
            self.rath[i] = mat1001 \
                           + (a_r + c_r * rath_param) * mat0010 \
                           + (a_t + (c_t * rath_param if i % 2 == 1 else b_t_glass * rath_param)) * mat0100

        for i, _ in enumerate(self.rath):
            RT = self.rath[i].to(device)
            n1 = self.materials[i - 1] if i > 0 else 1.0
            n2 = self.materials[i]
            n_outside, n_inside = (n1, n2) if RT.data[1, 0] > 0.0 else (n2, n1)

            unisurf_ = torch.matmul(
                mat1001 + RT * mat0100,
                torch.tensor([[1, 0], [(n_outside - n_inside) / n2, n1 / n2]], dtype=torch.float32).to(device)
                    * (mat1101 + (one / RT) * mat0010)
            )
            unisurf = unisurf_.to(device).matmul(unisurf.to(device)).to(device)

        x = torch.transpose(x, 0, 2)
        x = torch.reshape(x, (2, -1))
        # print(unisurf.size(), x.size())
        x = unisurf.matmul(x)# + torch.transpose(self.fc(torch.transpose(x, 0, 1)), 0, 1)# + torch.reshape(self.fc(torch.reshape(torch.vstack(self.rath), (-1,))), (2, -1))
        # print('ddd', x.size())

        y_1 = torch.unsqueeze(x[0, :], dim=0)
        y_2 = torch.unsqueeze(x6, dim=-1)
        y_4 = torch.matmul(y_2, torch.ones_like(y_1).to(device)) - torch.matmul(torch.ones_like(y_2).to(device), y_1)
        y_5 = torch.exp(- torch.square(y_4) / 2) / math.sqrt(2 * math.pi)
        # y_6 = torch.exp(- torch.square(x6) / 2) / math.sqrt(2 * math.pi)
        img = torch.sum(y_5, dim=-1)
        img = img / torch.sum(img, dim=-1)
        # img = torch.squeeze(torch.squeeze(img, dim=0), dim=0)
        # plt.plot(x6.cpu().detach().numpy(), img.cpu().detach().numpy())
        # plt.show()

        # print(unisurf.size(), x.size())
        # x = torch.sigmoid(x)
        # print(torch.tensor(torch.sum(torch.matmul(torch.nn.functional.one_hot(torch.tensor([1, 3], dtype=torch.int)), obj)), dtype=torch.float32))
        # print(torch.(x[:, 0], obj[:, 0], self.img_scale))
        # x = torch.stft()

        # x2 = x2_mat(x[0, :], x.size(-1))
        # a = torch.matmul(torch.inverse(x2), obj)
        # img = torch.matmul(x2_lin, a)
        #
        x2_ = torch.unsqueeze(x6, dim=0)
        nu_ = torch.unsqueeze(nu, dim=-1)

        Img = torch.sqrt(torch.square(torch.sum(img * torch.cos(torch.matmul(nu_, 2*math.pi*x2_)), dim=-1))
                       + torch.square(torch.sum(img * torch.sin(torch.matmul(nu_, 2*math.pi*x2_)), dim=-1)))
        # print(x2_lin, x2_lin.size())
        # plt.plot(nu.cpu().detach().numpy(), Img.cpu().detach().numpy())
        # plt.show()

        x = torch.transpose(x, 0, 1)
        # print(x.size())
        return x, Img


def loss_1(model, output, nu, Obj, Img):
    T = Img / Obj
    # return torch.var(output[:, 0], dim=-1)
    # return 1 / T[torch.where(abs(nu-30)<1.0)[0]]
    return 1 / torch.sum(T) + torch.var(output[:n_rays, 0], dim=-1)
    # + torch.var(output[..., 0]) * sum([torch.abs(torch.clamp(rt[0, 1], max=0.)) for rt in model.rath])\
    # + 0.5 * torch.abs(15 - model.thickness[-1][0, 1])


def loss_2(model, output, nu, Obj, Img):
    # T = Img / Obj
    return torch.var(output[:, 0], dim=-1)
    # return 1 / torch.sum(T)


def loss_3(rath):
    # T = Img / Obj
    return torch.ones_like(rath) * 1e-6
    # return 1 / torch.sum(T)


if __name__ == '__main__':
    loss_threshold = 1e-6
    epochs = 20000

    best_score = 0

    n_rays = 200
    n_points = 20
    beam_angle = math.tan(math.radians(17.5))
    n_dots = 300
    obj_dist = 100.0
    obj_height = 2.0
    img_height = 50
    ra_ = [99.248354, 1114.0, 99.248354, 1114.0, 88.504538, 336.957495]
    th_ = [2.629486, 20.343253, 2.629486, 20.343253, 14.486286, 105.0]
    # ra_ = [48.135209, -49.487523, 14.736591, -58.096546]
    # th_ = [2.026799, 12.056468, 4.949522, 40.000342-28.949797]
    index_of_refraction = [1.603101, 1.0, 1.582670, 1.0, 1.582670, 1.0]
    img_dist = th_[-1]
    width = obj_dist + sum(th_)

    # dx_lin = 1.0
    # x_ = torch.linspace(-2, 2, int(4 / dx_lin)).to(device)
    x6 = torch.linspace(0.0, obj_height, 10000).to(device)
    # x_ = torch.linspace(-2, 2, 1000).to(device)
    # x2_lin = x2_mat(x_, n_points * n_rays)
    # x_ = torch.unsqueeze(x_, dim=0)
    nu = torch.linspace(0.0, 30, 1000).to(device)
    # nu2 = torch.linspace(0.1, 20, 80).to(device)
    # nu_lin = x2_mat(nu, 1000)
    # nu = torch.unsqueeze(nu, dim=-1)

    model = OpticalModel(obj_dist, index_of_refraction, n_points, img_height).to(device)

    criterion = loss_1
    criterion_2 = loss_2
    criterion_3 = loss_3
    optimizer = torch.optim.Adadelta(model.parameters(), lr=1e-5)
    # scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=1, gamma=0.5)

    for i, (r, t) in enumerate(zip(ra_, th_)):
        model.rath[i].data[1, 0] = r
        model.rath[i].data[0, 1] = t

    for RT in model.rath:
        print('R:', RT.data[1, 0], 'T:', RT.data[0, 1], end=' | ')
    print()

    obj2 = 1 + torch.sin(x6 * 2 * math.pi * 10 * x6)
    obj2 = obj2 / torch.sum(obj2, dim=-1)

    for epoch in range(epochs):

        rays = torch.reshape(torch.cat([torch.transpose(torch.vstack([torch.ones(n_rays) * obj_h,
                                          torch.linspace(math.tan(math.radians(-beam_angle)),
                                                      math.tan(math.radians(beam_angle)), n_rays)]).to(device), 0, 1)
                for obj_h in torch.linspace(0.1, obj_height, n_points)], dim=0), (n_points, n_rays, 2))
        # obj = 1e-10 * torch.sin(torch.linspace(0, obj_height, n_points * n_rays) * 60).to(device)

        # x4 = x2_mat(obj, 1000)
        # x5 = torch.matmul(x2_mat(x_, 1000), torch.matmul(torch.inverse(x4), obj2))int(4 / dx_lin)
        # print(obj2)
        # obj = 1e-4 * torch.sin(torch.linspace(0.1, obj_height, n_points * n_rays) * torch.linspace(0.1, 100, n_points * n_rays)).to(device)
        # print(obj)

        # obj3 = 1e-4 * torch.sin(torch.linspace(0.1, obj_height, int(4 / dx_lin)) * torch.linspace(0.1, 100, int(4 / dx_lin))).to(device)

        # plt.plot(x6.cpu().detach().numpy(), obj2.cpu().detach().numpy())
        # plt.show()

        # img = torch.squeeze(torch.squeeze(obj2_, dim=0), dim=0)
        # print(obj2, obj2_)
        # plt.plot(x6.cpu().detach().numpy(), obj2.cpu().detach().numpy())
        # plt.show()

        # obj = torch.reshape(torch.cat([torch.ones(n_rays).to(device) * 1e-10 * torch.sin(obj_h * 60).to(device)
        #                                for obj_h in torch.linspace(0, obj_height, n_points)], dim=0), (-1,))
        # print(obj.size(), nu.size(), x_.size(), dx_lin)

        # x2_ = torch.linspace(0, obj_height, 1000).to(device)
        # x2 = x2_mat(x2_, x2_.size(-1))
        # a = torch.matmul(torch.inverse(x2), obj2)
        #
        # x2_lin_ = x2_mat(x_, 1000)
        # obj_ = torch.matmul(x2_lin_, a)

        x3 = torch.unsqueeze(x6, dim=0)
        nu_ = torch.unsqueeze(nu, dim=-1)
        # print(x3.size(), obj_.size(), nu_.size())

        Obj = torch.sqrt(torch.square(torch.sum(obj2 * torch.cos(torch.matmul(nu_, 2*math.pi*x3)), dim=-1))
                         + torch.square(torch.sum(obj2 * torch.sin(torch.matmul(nu_, 2*math.pi*x3)), dim=-1)))

        # print('kkk', torch.matmul(torch.ones_like(obj_), torch.unsqueeze(obj_, dim=0)), torch.sum(torch.sin(torch.matmul(nu, 2*math.pi*x3)), dim=-1).size())

        output, Img = model(rays, obj2)

        # plt.ylim(0, 1e6)
        # Obj = torch.clamp(Obj, min=0, max=1e3)
        # plt.plot(nu.cpu().detach().numpy(), Obj.cpu().detach().numpy())
        # plt.show()
        # plt.plot(nu.cpu().detach().numpy(), torch.clamp(Img / Obj, min=0, max=1).cpu().detach().numpy())
        # plt.show()

        # Img = torch.clamp(Img, min=0, max=1e3)
        # plt.plot(nu.cpu().detach().numpy(), Img.cpu().detach().numpy())
        # plt.show()

        loss = criterion(model, output, nu, Obj, Img)


        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        # scheduler.step()

        score = float(torch.sum(Img / Obj))

        if score > best_score:
            best_score = score
            # scheduler.step()

        width = obj_dist + sum([float(RT.data[0, 1]) for RT in model.rath])

        if loss.item() < loss_threshold:
            print('Epoch [{}/{}], Loss: {:.5f}'.format(epoch + 1, epochs, loss.item()))
            print("The loss value is reached")

            # for i in range(len(model.rath_param)):
            #     # model.rath_param[i].data = torch.rand(size=(128,)).to(device)
            #     model.rath_param[i].data = torch.rand(size=(2, 2)).to(device)

            # obj_height = random.uniform(-2.0, 2.0)

        elif (epoch + 1) % 10 == 0:
            with open('results.txt', 'at', encoding='utf-8') as file:
                for RT in model.rath:
                    file.write('R:' + str(RT.data[1, 0]) + '\tT:' + str(RT.data[0, 1]) + '\n')
                file.write('score:' + str(best_score) + '\n\n')

            print('Epoch: [{}/{}], Loss:{:.5f}'.format(epoch + 1, epochs, loss.item()), 'score:', score)

        if (epoch + 1) % 100 == 0:
            for RT in model.rath:
                print('R:', RT.data[1, 0], 'T:', RT.data[0, 1])
            # print(output)

            T = Img / Obj
            T = torch.clamp(T, min=0, max=1)
            b, a = butter(8, 0.04, 'lowpass')   #配置滤波器 8 表示滤波器的阶数
            plt.plot(nu.cpu().detach().numpy(), scipy.signal.filtfilt(b, a, T.cpu().detach().numpy()))
            plt.show()

            # trace = torch.zeros((n_dots, n_points * n_rays, 2))
            trace = torch.zeros((n_dots, n_points * 2, 2))
            # trace[0, :, :] = torch.reshape(rays, (-1, 2)).to(device).detach()
            trace[0, :, :] = torch.cat([torch.reshape(rays, (-1, 2))[::n_rays, :], torch.reshape(rays, (-1, 2))[n_rays-1::n_rays, :]], dim=0).to(device).detach()

            # for i1 in range(n_points * n_rays):
            for i1 in range(n_points):
                i2 = 0
                x = 0
                thickness = 0

                while x + width / n_dots < thickness + obj_dist and i2 + 1 < n_dots:
                    trace[i2 + 1, i1, :] = torch.tensor([[1, width / n_dots], [0, 1]]).matmul(trace[i2, i1, :]).cpu().detach()
                    i2 += 1
                    x += width / n_dots

                i2 = int(obj_dist/(width/n_dots))
                x = obj_dist
                thickness = obj_dist

                for i, _ in enumerate(model.rath):
                    RT = model.rath[i]
                    n1 = model.materials[i - 1] if i > 0 else 1.0
                    n2 = model.materials[i]
                    n_outside, n_inside = (n1, n2) if RT.data[1, 0] > 0.0 else (n2, n1)
                    surf = torch.tensor([[1, 0], [(n_outside - n_inside) / n2, n1 / n2]], dtype=torch.float32).to(device) \
                           * (mat1101 + (one / RT) * mat0010).to(device)

                    if i2 + 1 < n_dots:
                        trace[i2 + 1, i1, :] = surf.matmul(trace[i2, i1, :].to(device)).cpu().detach()
                        i2 += 1
                        x += width / n_dots

                    while x + width / n_dots < thickness + RT.data[0, 1] and i2 + 1 < n_dots:
                        trace[i2 + 1, i1, :] = torch.tensor([[1, width / n_dots], [0, 1]]).to(device).matmul(trace[i2, i1, :].to(device)).cpu().detach()
                        i2 += 1
                        x += width / n_dots

                    thickness += RT.data[0, 1]

                while i2 + 1 < n_dots:
                    trace[i2 + 1, i1, :] = torch.tensor([[1, width / n_dots], [0, 1]]).to(device).matmul(torch.tensor(trace[i2, i1, :], dtype=torch.float32).to(device)).cpu().detach()
                    i2 += 1
                    x += width / n_dots

            # print(trace)
            # plt.ylim(-15, 15)

                # for i1 in range(n_points * n_rays):
            for i1 in range(n_points*2):
                plt.plot(np.arange(obj_dist, step=width/n_dots, stop=width), np.array(trace[int(obj_dist/(width/n_dots)):, i1, 0]))
            plt.show()

        if loss.item() < loss_threshold:
            break
