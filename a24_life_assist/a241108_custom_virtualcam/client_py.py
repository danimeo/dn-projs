from PIL import Image
from io import BytesIO
import requests
url = "图片链接的url"
response = requests.get(url)
im = Image.open(BytesIO(response.content))
img_byte = BytesIO()
im.save(img_byte, format='JPEG') # format: PNG or JPEG
binary_content = img_byte.getvalue()  # im对象转为二进制流
