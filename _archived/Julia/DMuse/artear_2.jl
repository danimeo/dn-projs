
`

前提知识：

张量中一般最后一维度为样本数量，如(784,N)

softmax与线性模型的区别在于最后目标函数是负对数似然

数据集标准形式为(..,N)，x和y合并成训练形式(xi,yi)，训练形式的xi（yi）为从x（yi）中抽取lengthofbatch个构成

`



`GZip需要提前安装`

using Knet,GZip

`定义模型：

#nll(~,~)用于计算Negative Log-Likelihood(负对数似然)，[预测值（前）减真实值（后）]，用作损失函数。

#w[1]为(10,784)大小，w[2]为(10,1)大小

#x为(28,28,1,sizeofbatch)大小，通过mat转化为(784,sizeofbatch)；y0为(sizeofbatch,)大小`

predict(w,x)=w[1]*mat(x) .+ w[2]

loss(w,x,y0)=nll(predict(w,x),y0)`预测为(10*sizeofbatch)大小，真实值为(sizeofbatch,)大小`

lossgrad=grad(loss)

function train(w,data;lr=0.1)

    for (xtrb,ytrb) in data

        print(size(ytrb))

        dw=lossgrad(w,xtrb,ytrb)

        w-=lr.*dw

    end

    return w

end

`#minibatch将数据集张量转化为小批量的数据集[(xi,yi)...]，可混洗。第三个参数为每批的大小。

#x~为(28*28*1*N)，y~为长度为N的Uint8`

include(Knet.dir("data/mnist.jl"))

xtrn,ytrn,xtst,ytst=mnist()

dtrn=minibatch(xtrn,ytrn,100)

dtst=minibatch(xtst,ytst,100)

#

w=Any[0.1f0*randn(Float32,10,784),zeros(Float32,10,1)]

println((:epoch, 0, :trn, accuracy(w,dtrn,predict), :tst, accuracy(w,dtst,predict)))

train(w, dtrn; lr=0.5)

for epoch=1:10

    train(w, dtrn; lr=0.5)

    println((:epoch, epoch, :trn, accuracy(w,dtrn,predict), :tst, accuracy(w,dtst,predict)))

end

