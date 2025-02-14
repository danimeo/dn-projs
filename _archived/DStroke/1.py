import subprocess as sp

sp.call(executable='C:\\conda\\Scripts\\stcgal.exe', args=r' -P stc89 -l 9600 -p COM5 "B:\codes\e\DAutoFlash\template.hex"')
# sp.call(executable='C:\\conda\\python.exe', args=' "C:\\conda\\Lib\\stcflash.py" --port COM5 --lowbaud 4800 --protocol 89 B:\\codes\\e\\C51_01\\Objects\\main.HEX')
# sp.call(executable='C:\\conda\\python.exe', args=' "C:\\conda\\Lib\\stcflash.py" --port COM5 --lowbaud 9600 --protocol 89 C:\\Users\\benoe\\Documents\\Xfer\\Objects\\2.hex')

