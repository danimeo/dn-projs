using CUDA

a = CUDA.zeros(Int(1e8))
b = CUDA.rand(Int(1e8))

c = a .+ b

