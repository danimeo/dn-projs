using HDF5

c = h5open("mydata.h5", "r") do file
    read(file, "A")
end
