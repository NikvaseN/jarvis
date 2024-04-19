import subprocess
import os
from modules.functions import starting, error

code_path = r'C:\Users\User0\AppData\Local\Programs\Microsoft VS Code\Code.exe'

def startDegree() :
	try:
		starting()
		subprocess.Popen([code_path])

		subprocess.Popen(["cmd", "/C", "cd C:/Users/User0/Desktop/degree-work/project & npm run client"], creationflags=subprocess.CREATE_NEW_CONSOLE)
		subprocess.Popen(["cmd", "/K", "cd C:/Users/User0/Desktop/degree-work/project & npm run server"], creationflags=subprocess.CREATE_NEW_CONSOLE)
	except:
		error()