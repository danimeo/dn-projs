using Distributed

max_total_delay = 0.5

mutable struct Element
    rela::Function
    links_to::Array{Pair{UInt32, Float16}}
end

a, attention = Dict(), Dict()

function rand_ele()
    rela(x) = x^2 + 2
    return Element(rela, [rand(UInt8) => rand(Float16) * 0.1])
end

for i = 1:1e+3
    addr = rand(UInt8)
    ele = rand_ele()
    a[addr] = ele
end

function distance(addr1, addr2, attention)
    if addr1 == addr2
        return 0
    else
        Sqrt_ = [sqrt((a[addr1].rela(x) - a[addr2].rela(x)) ^ 2) for x = -50:0.25:50] .* attention[addr1]
        println(Sqrt_)
        sum = 0
        for sqrt_ = Sqrt_
            sum += sqrt_
        end
        println(length(Sqrt_))
        return sum / length(Sqrt_)
    end
end

function add_to_attention(addr, prev_delay)
    attention[addr] = prev_delay
    sum = 0
    for value = values(attention)
        sum += value
    end
    while sum > max_total_delay
        println("attention已满：", string(addr, base=16), " sum=", sum, " max_total_delay=", max_total_delay)
        dmax_key = 0
        for key = keys(attention)
            println("addr=", addr, " key=", key)
            d = distance(addr, key, attention)
            if d > dmax
                dmax_key = key
            end
        end
        println("__attention=", attention)
        sum -= attention[dmax_key]
        delete!(attention, dmax_key)
        println("已删除：", dmax_key)
    end
    println(string(addr, base=16), " ", prev_delay)
end

function associate(start_addr)
    if start_addr in keys(a)
        for pair = values(a[start_addr].links_to)
            addr = pair.first
            delay = pair.second
            println(addr)
            add_to_attention(addr, delay)
            sleep(delay * 10)
            @async associate(addr)
        end
    else
        a[start_addr] = rand_ele()
        @async associate(start_addr)
    end
end

associate(1)
