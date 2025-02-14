using CUDA

use_gpu = true

mutable struct Placeholder
    name::Symbol
    Placeholder() = begin
        new(:output)
    end
end

mutable struct Link
    from::Symbol
    to::Symbol
end

mutable struct Neuron
    input::Placeholder
    weights::CuArray
    output::Link
    Neuron() = begin
        new(Placeholder(), CUDA.zeros(4), Link(:input, :output))
    end
end

function +(a::Neuron, b::Neuron)
    c = Neuron()
    println(typeof(CuArray(a.weights)))
    c.weights = CUDA.zeros(4) .+ CUDA.ones(4)
    return c
end

a = Neuron()
b = Neuron()
a.weights = CuArray{Float64, 1}([1;2;3;4])
b.weights = CuArray{Float64, 1}([1;2;3;4])
c = a + b
c.weights