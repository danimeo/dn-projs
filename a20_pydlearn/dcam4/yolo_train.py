from ultralytics import YOLO

model = YOLO('yolov8m-cls.yaml')  # build a new model from YAML
model.train(data=r'B:\codes\ds\DLearn\pydlearn\dcam4\dataset', epochs=2, workers=0, batch=1)
