options = trainingOptions('sgdm', ... %优化器
    'LearnRateSchedule','piecewise', ... %学习率
    'LearnRateDropFactor',0.2, ... % 
    'LearnRateDropPeriod',5, ...
    'MaxEpochs',20, ... %最大学习整个数据集的次数
    'MiniBatchSize',128, ... %每次学习样本数
    'Plots','training-progress'); %画出整个训练过程

doTraining = true; %是否训练
if doTraining
    trainNet = trainNetwork(XTrain, YTrain,layers,options);
    % 训练网络，XTrain训练的图片，YTrain训练的标签，layers要训练的网
    % 络，options训练时的参数
end
save Minist_LeNet5 trainNet %训练完后保存模型
yTest = classify(trainNet, XTest); % 测试训练后的模型
accuracy = sum(yTest == YTest)/numel(YTest); %模型在测试集的准确率
