using Knet
using NPZ



# Define convolutional layer:
struct Conv; w; b; end
Conv(w1,w2,nx,ny) = Conv(param(w1,w2,nx,ny), param0(1,1,ny,1))
(c::Conv)(x) = relu.(pool(conv4(c.w, x) .+ c.b))

# Define dense layer:
struct Dense; w; b; f; end
Dense(i,o; f=identity) = Dense(param(o,i), param0(o), f)
(d::Dense)(x) = d.f.(d.w * mat(x) .+ d.b)

# Define a chain of layers and a loss function:
struct Chain; layers; end
(c::Chain)(x) = (for l in c.layers; x = l(x); end; x)
(c::Chain)(x,y) = nll(c(x),y)



data_gen_dir = "C:/dev_spa/artear_1/data_gen"
dat_tr = npzread(data_gen_dir * "/input_data.npy")
dat_tr_n = npzread(data_gen_dir * "/output_n_data.npy")
dat_tr_d = npzread(data_gen_dir * "/output_d_data.npy")
dat_tr_t = npzread(data_gen_dir * "/output_t_data.npy")


LeNet = Chain(
    (Conv(5,5,1,20),
    Conv(5,5,20,50),
    Dense(800,500,f=relu),
    Dense(500,10, f=softmax)))


dtrn = minibatch(dat_tr, [dat_tr_n, dat_tr_d, dat_tr_t], 10)
print(dtrn)

# progress!(adam(LeNet, ncycle(dat_tr,3)))
# accuracy(LeNet,data=dtst)



println(size(dat_tr))
