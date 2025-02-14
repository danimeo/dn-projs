
function X = test2()
    a = preprocess('C:\\projects\\pycharm_projects\\mazerunner\\data\\b27_acc_50ms_rt_4_filtered_a.txt');
    X = a;
end

function X = preprocess(filename)
    fileID = fopen(filename, 'r', 'n', 'GB2312');
    disp(fileID);
    %a = textread(filename, '%d8 %d');
    X = a;
    fclose(fileID);
end
