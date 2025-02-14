# USB\VID_2D37&PID_3DBE
from escpos.printer import Usb, Serial
import usb.core
import usb.util

id_vendor, id_product = 0x2d37, 0x3dbe
# # 查找USB设备
# dev = usb.core.find(idVendor=id_vendor, idProduct=id_product)

# if dev is None:
#     raise ValueError("Device not found")
# else:
#     print("Device found")

# # set the active configuration. With no arguments, the first
# # configuration will be the active one
# dev.set_configuration()

# # get an endpoint instance
# cfg = dev.get_active_configuration()
# intf = cfg[(0,0)]

# ep = usb.util.find_descriptor(
#     intf,
#     # match the first OUT endpoint
#     custom_match = \
#     lambda e: \
#         usb.util.endpoint_direction(e.bEndpointAddress) == \
#         usb.util.ENDPOINT_OUT)
# ep_in = usb.util.find_descriptor(
#     intf,
#     # match the first IN endpoint
#     custom_match = \
#     lambda e: \
#         usb.util.endpoint_direction(e.bEndpointAddress) == \
#         usb.util.ENDPOINT_IN)
# print(ep_in, ep)
# assert ep_in is not None, ep is not None

# # write the data
# ep.write('test')
   
# 原文链接：https://blog.csdn.net/weixin_42967006/article/details/108755972

# Device found
#       ENDPOINT 0x2: Bulk OUT ===============================
#        bLength          :    0x7 (7 bytes)
#        bDescriptorType  :    0x5 Endpoint
#        bEndpointAddress :    0x2 OUT
#        bmAttributes     :    0x2 Bulk
#        wMaxPacketSize   :   0x40 (64 bytes)
#        bInterval        :    0x0

p = Usb(id_vendor, id_product,  timeout=0, in_ep=0x82, out_ep=0x2)
# p.
# p = Serial('COM3', 38400, timeout=1)
p.text("Hello world\n")
print(p.is_online(), p.is_usable())
# p._raw(b'\x1B\x40')
p.text("Hello World\n")
# p.image("logo.gif")
# p.barcode('4006381333931', 'EAN13', 64, 2, '', '')
p.cut()
p.close()
