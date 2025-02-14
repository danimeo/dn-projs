sr3 = serialport('COM7', 115200);       % 使用默认设置创建串口sr3
fopen(sr3);                 %打开串口
count = [];
for duty = 0:0.5:60
    num1=single([duty, duty]);
    write(sr3, typecast(num1,'uint8'), 'uint8');         % 给串口写入数据
    count = fscanf(sr3);           %读取串口数据（无分号，可在Matlab工作区实时查看）
    disp(count);
end
fclose(sr3);                %关闭串口
delete(sr3);
clear sr3;