datapath = "./Mnist/";

filenameImagesTrain = strcat(datapath, "train-images-idx3-ubyte");
filenameLabelsTrain = strcat(datapath, "train-labels-idx1-ubyte");
filenameImagesTest = strcat(datapath, "t10k-images-idx3-ubyte");
filenameLabelsTest = strcat(datapath, "t10k-labels-idx1-ubyte");

XTrain = processMNISTimages(filenameImagesTrain);
YTrain = processMNISTlabels(filenameLabelsTrain);
XTest = processMNISTimages(filenameImagesTest);
YTest = processMNISTlabels(filenameLabelsTest);
% 处理Mnist数据集图像
function X = processMNISTimages(filename)
    [fileID,errmsg] = fopen(filename,'r','b');
    if fileID < 0
        error(errmsg);
    end
    magicNum = fread(fileID,1,'int32',0,'b');
    if magicNum == 2051
        fprintf('\nRead MNIST image data...\n')
    end
    numImages = fread(fileID,1,'int32',0,'b');
    fprintf('Number of images in the dataset: %6d ...\n',numImages);
    numRows = fread(fileID,1,'int32',0,'b');
    numCols = fread(fileID,1,'int32',0,'b');
    X = fread(fileID,inf,'unsigned char');
    X = reshape(X,numCols,numRows,numImages);
    X = permute(X,[2 1 3]);
    X = X./255;
    X = reshape(X, [28,28,1,size(X,3)]);
    X = dlarray(X, 'SSCB');
    fclose(fileID);
end
% 处理Mnist数据集标签
function Y = processMNISTlabels(filename)
    [fileID,errmsg] = fopen(filename,'r','b');
    if fileID < 0
        error(errmsg);
    end
    magicNum = fread(fileID,1,'int32',0,'b');
    if magicNum == 2049
        fprintf('\nRead MNIST label data...\n')
    end
    numItems = fread(fileID,1,'int32',0,'b');
    fprintf('Number of labels in the dataset: %6d ...\n',numItems);
    Y = fread(fileID,inf,'unsigned char');
    Y = categorical(Y);
    fclose(fileID);
end
