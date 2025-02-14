using Distributed
using Dates
using Plots
import Plots:plot

attention_capacity = 20000

#nodes = Dict(i=>Dict(UInt16(rand(1:65535))=>Float64(0.0) for n = 1:rand(3:25)) for i::UInt16 = 1:65535)
nodes = Dict(i=>Dict(i + UInt16(1)=>Float64(0.0) for n = 1:1) for i::UInt16 = 1:95)
nodes[95] = Dict(1=>Float64(0.0))
#nodes[95] = Dict()

init = UInt16(1), UInt16(rand(keys(nodes[1])))
init_level = Float64(1.0)
#rnd = rand(keys(nodes))
#receiver = (rnd, UInt16(rand(keys(nodes[rnd]))))
receiver = (UInt16(44), UInt16(45))
println("init: ", string.(init))
println("receiver: ", string.(receiver))

nodes[init[1]][init[2]] = init_level
attention = Dict{Tuple{UInt16, UInt16}, Float64}((init[2], init[1])=>init_level)
attention_buffer = Pair{Tuple{UInt16, UInt16}, Float64}[]
asso_count = 0
init_time = now()

function associate(start::UInt16, input_level::Float64)
    global asso_count
    asso_count += 1
    targets = keys(nodes[start])
    #println("Current node: " * string(start) * " [" * string(targets) * "]")

    S = (input_level + sum(nodes[start][targ] for targ = targets)) / 2

    aver = S / length(targets)
    for target = targets
        d::Float64 = abs(nodes[start][target] - aver)
        nodes[start][target] = aver
        if length(attention) + length(attention_buffer) + 1 > attention_capacity
            continue
        end
        push!(attention_buffer, (target, start)=>d)
    end

    return S
end

function process()
    #println("attention: " * string(length(attention)) * "; count: " * string(asso_count))

    if ! isempty(attention)
        kys = sort(collect(keys(attention)), rev=true, by=key->attention[key])
        for (node, prev) = kys
            #if attention[(node, prev)] < 1e-6
            #    delete!(attention, (node, prev))
            #    continue
            #end
            nodes[prev][node] = associate(node, nodes[prev][node])
            delete!(attention, (node, prev))
        end
    end
        
    if ! isempty(attention_buffer)
        merge!(attention, Dict(attention_buffer))
        empty!(attention_buffer)
    end
    
    if ! isempty(attention) || ! isempty(attention_buffer)
        sleep(0.001)
        schedule(Task(process))
    end
end

function apply_func(f::Function, x::Float64)
    level = f(x)
    nodes[init[1]][init[2]] = level
    associate(init[2], level)
    nodes[receiver[1]][receiver[2]]
end

f(x) = 10.0 * sin(0.8 * x)

gr(show = true)
f_pairs = Pair{Float64, Float64}[]

function update()
    global f_pairs
    now_ = Dates.value(Nanosecond(now() - init_time)) * 1e-9
    append!(f_pairs, [now_=>apply_func(f, now_)])
    if length(f_pairs) > 1000
        popfirst!(f_pairs)
    end
    [pair[1] for pair in f_pairs], [pair[2] for pair in f_pairs]
end

schedule(Task(process))

while true
    t, f_val = update()
    display(plot(t, f_val))
    sleep(0.001)
end




