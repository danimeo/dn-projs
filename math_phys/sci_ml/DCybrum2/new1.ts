import { Tensor, InferenceSession } from "onnxjs";
 
async function start() {
    const session = new InferenceSession();
    await session.loadModel('./models/model.onnx');
 
    const inputs = [new Tensor(new Float32Array(/* 模型所需输入数据 */), 'float32', [/* 输入形状 */])];
    const outputMap = await session.run(inputs);
    const outputTensor = outputMap.values().next().value;
    console.log('模型输出:', outputTensor.data);
}
start();
