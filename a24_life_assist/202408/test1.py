from wakeonlan import send_magic_packet

send_magic_packet("40:16:7E:66:23:F5".replace(':', '.'))

# send_magic_packet("40.16.7e.66.23.f5".replace(':', '.'))
