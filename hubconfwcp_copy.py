import base64
from pathlib import Path
from datetime import datetime
import cv2
import torch
import os
import img_ocr
from models.yolo import Model
from utils.general import check_requirements, set_logging
from utils.google_utils import attempt_download
from utils.torch_utils import select_device

dependencies = ['torch', 'yaml']
check_requirements(Path(__file__).parent / 'requirements.txt', exclude=('pycocotools', 'thop'))
set_logging()


def create(name, pretrained, channels, classes, autoshape):
    try:
        cfg = list((Path(__file__).parent / 'cfg').rglob(f'{name}.yaml'))[0]  # model.yaml path
        model = Model(cfg, channels, classes)
        if pretrained:
            fname = f'{name}.pt'  # checkpoint filename
            attempt_download(fname)  # download if not found locally
            ckpt = torch.load(fname, map_location=torch.device('cpu'))  # load
            msd = model.state_dict()  # model state_dict
            csd = ckpt['model'].float().state_dict()  # checkpoint state_dict as FP32
            csd = {k: v for k, v in csd.items() if msd[k].shape == v.shape}  # filter
            model.load_state_dict(csd, strict=False)  # load
            if len(ckpt['model'].names) == classes:
                model.names = ckpt['model'].names  # set class names attribute
            if autoshape:
                model = model.autoshape()  # for file/URI/PIL/cv2/np inputs and NMS
        device = select_device('0' if torch.cuda.is_available() else 'cpu')  # default to GPU if available
        print(device)
        return model.to(device)

    except Exception as e:
        s = 'Cache maybe be out of date, try force_reload=True.'
        raise Exception(s) from e


def custom(path_or_model='path/to/model.pt', autoshape=True):
    model = torch.load(path_or_model, map_location=torch.device('cpu')) if isinstance(path_or_model,
                                                                                      str) else path_or_model  # load checkpoint
    if isinstance(model, dict):
        model = model['ema' if model.get('ema') else 'model']  # load model
    hub_model = Model(model.yaml).to(next(model.parameters()).device)  # create
    hub_model.load_state_dict(model.float().state_dict())  # load state_dict
    hub_model.names = model.names  # class names
    if autoshape:
        hub_model = hub_model.autoshape()  # for file/URI/PIL/cv2/np inputs and NMS
    device = select_device('0' if torch.cuda.is_available() else 'cpu')  # default to GPU if available
    return hub_model.to(device)


def yolov7(pretrained=True, channels=3, classes=80, autoshape=True):
    return create('yolov7', pretrained, channels, classes, autoshape)


def crop_image_by_center(image, center, width, height):
    # 计算左上角和右下角坐标
    x = int(center[0] - width / 2)
    y = int(center[1] - height / 2)
    top_left = (x, y)
    bottom_right = (x + width, y + height)

    # 截取图像子区域
    cropped_image = image[y:y + height, x:x + width]

    # 返回裁剪后的图像
    return cropped_image
def save_error_image(cropped_image):
    if not os.path.exists("error_image"):
        os.makedirs("error_image")
    try:
        filename = f"error_image/{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        success = cv2.imwrite(filename, cropped_image)
        if success:
            print(f"Image successfully saved as {filename}")
        else:
            print("Failed to save image")
    except Exception as e:
        print(f"Exception occurred: {e}")

def process_frame(model, frame):
    # 这里进行帧的处理
    timestemp = datetime.now().strftime("%Y-%m-%d|%H:%M:%S")
    results = model([frame])
    has_train=False
    if results.xywh[0].shape[0] <= 0:
        return timestemp, 0, 0 ,has_train
    else:
        for idx, obj in enumerate(results.xywh[0]):
            # frames[idx]
            has_train=True
            obj = obj.cpu().numpy().astype(int)
            cropped_image = crop_image_by_center(frame, (obj[0], obj[1]), obj[2], obj[3])
            

            height, width = frame.shape[:2]    
            print(f'Frame Height: {height}, Frame Width: {width}')
            

            x = int(obj[0] - obj[2] / 2)
            y = int(obj[1] - obj[3] / 2)
            top_left = (x, y)
            bottom_right = (x + obj[2], y + obj[3])

            text = img_ocr.imgocr(cropped_image)
            if text is None or text=='None':
                save_error_image(cropped_image)
            _, buffer = cv2.imencode('.jpg', frame)
            #base64_image = base64.b64encode(buffer).decode('utf-8')
            # message = {"camera-id":current_id,"image": base64_image,"timestemp": datetime.now().strftime("%Y-%m-%d|%H:%M:%S"), "text": text}

            # if timestemp is not None and text is not None:
            #     print(timestemp + " " + text+" "+str(camera_id))
            return timestemp, text, 1 ,has_train, top_left,bottom_right

