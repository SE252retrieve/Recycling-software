import base64
import torch, glob, cv2
import numpy as np
import torch.nn as nn
import torch.nn.functional as F
from torchvision import models, transforms
import os
from bottle import run,template,route,request

classes = ['书包',
           '塑料瓶',
           '塑料餐盒',
           '手机',
           '易拉罐',
           '橡皮',
           '毛巾',
           '毛绒玩具',
           '泡沫塑料',
           '玻璃瓶',
           '电池',
           '笔',
           '笔记本电脑',
           '纸',
           '罐头盒',
           '衣服'
           ]
def predict_one_img(img_path):
    device = torch.device("cpu")
    model_path = "dataset_pytorch_20220814.pth"
    net = torch.load(model_path,map_location=torch.device('cpu'))
    img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), 1)
    img = cv2.resize(img, (224, 224))
    # 把图片由BGR变成RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # 1.将numpy数据变成tensor
    tran = transforms.ToTensor()
    img = tran(img)
    img = img.to(device)
    # 2.将数据变成网络需要的shape
    img = img.view(1, 3, 224, 224)
    out1 = net(img)
    out1 = F.softmax(out1, dim=1)
    proba, class_ind = torch.max(out1, 1)
    class_ind = int(class_ind)
    return classes[class_ind]


@route('/<name>', method='POST')
def index(name):
    try:
        if (name == 'classify'):
            data = request.body.read()
            data = base64.b64decode(data)
            open('1.png', 'wb').write(data)
            results = predict_one_img("1.png")
            print(name, results)

            return '{}'.format(results)
        else:
            print('error', name)
            return '-1'
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    run(host='0.0.0.0', port=80)
