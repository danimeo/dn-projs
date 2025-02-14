import requests


# def getIPv6Address():
#     # text = requests.get('http://getip6.china-ipv6.cn:5010/').text
#     text = requests.get('https://v6.ident.me').text
#     return text

import os
import re


def getIPv6Address():
    output = os.popen("ipconfig /all").read()
    # print(output)
    result = re.findall(r"(([a-f0-9]{1,4}:){7}[a-f0-9]{1,4})", output, re.I)
    return result[0][0]



if __name__ == "__main__":
    print(getIPv6Address())
