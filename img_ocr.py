import re
import easyocr

def check_string(input_string):
    pattern = r"0\d{2}"  # 匹配以0开头的连续三个数字
    match = re.findall(pattern, input_string)
    if match:
        return match[0]  # 输出匹配到的连续三个数字
    else:
        return None

def imgocr(image):
    # 读取图像文件并进行OCR识别
    reader = easyocr.Reader(['en'])
    result = reader.readtext(image)
    # 获取识别的文本
    text = [res[1] for res in result]
    # 打印识别的文本
    # print(text[0])
    if len(text) > 0:
        return check_string(text[0])


