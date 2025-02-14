#=
Trial2:
- Julia version: 
- Author: Dajun
- Date: 2021-10-08
=#

using LibSerialPort, Plots
const small_pack_header = (0xaa, 0xaa, 0x04, 0x80, 0x02)


function read_data()
    t = time()
    arr = Float64[]
    time_arr = Float64[]

    println("正在预编译LibSerialPort库")

    tsk = @task begin
        LibSerialPort.open("COM3", 10240) do io
            println("正在读取数据：")
            buffer = zeros(UInt8, 8)
            while true
                read!(io, buffer)
                while false in (buffer[1:5] .== small_pack_header)
                    popfirst!(buffer)
                    push!(buffer, read(io, UInt8))
                end
                raw_data = (Int16(buffer[6]) << 8) | Int16(buffer[7])
                # if raw_data > 0x8000 raw_data -= 0x10000 end
                if buffer[8] != (xor(0x82 + buffer[6] + buffer[7], 0xffff) & 0xff)
                    continue
                end
                push!(time_arr, time() - t)
                push!(arr, Float64(raw_data) / 2048.)
            end
        end
    end

    schedule(tsk)

    while true
        while time_arr[end] - time_arr[1] < 1.
            popfirst!(time_arr)
            popfirst!(arr)
        end
        display(plot(time_arr, arr))
        sleep(0.05)
    end
end

read_data()

