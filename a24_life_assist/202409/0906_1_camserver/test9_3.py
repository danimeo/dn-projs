import requests

def get_image_from_url(url):
    res = requests.get(url)
    return res.content


img = get_image_from_url("http://192.168.4.62")
# img = requests.post("http://192.168.4.62/", data=img))
print(img)
