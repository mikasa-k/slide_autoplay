# サークル紹介用 半自動プレゼンテーションランチャー
# パワポが大半なので、このランチャーもwindows前提です
import sys
import os
import subprocess
import winreg

#絶対パス取得
d_root = os.path.abspath(os.path.dirname(sys.argv[0]))

#フリーズ対策
is_wait = False

#実行ソフトの検出
def find_program_file(program_name):
	name = program_name.lower()
	n = ""
	idr = None
	paths = []
	if name == "powerpoint":
		paths = [
		r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\POWERPNT.EXE",
		r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\App Paths\POWERPNT.EXE"]
	elif name == "libreoffice":
		paths = [
		r"SOFTWARE\LibreOffice\UNO\InstallPath",
		r"SOFTWARE\WOW6432Node\LibreOffice\UNO\InstallPath"]
		n = r"\soffice.exe"
	elif name == "vlc":
		paths = [
		r"SOFTWARE\VideoLAN\VLC",
		r"SOFTWARE\WOW6432Node\VideoLAN\VLC"]
		n = r"\vlc.exe"
		idr = "InstallDir"
	for p in paths:
		try:
			key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, p)
			value, _ = winreg.QueryValueEx(key, idr)
			return value+n
		except (e):
			print(e)
			pass
	return False
def play(file_name, cmd):
	global is_wait
	if cmd[0] == False:
		print("can not open %s"% file_name)
		return False
	try:
		print("EXECUTE:%s"% " ".join(cmd))
		is_wait = True
		p = subprocess.Popen(cmd)
		p.wait()
	except:
		pass
	is_wait = False
	return True
def load(d_root):
	programs = {}
	cmds = []
	for i in ["powerpoint","libreoffice","vlc"]:
		p = find_program_file(i)
		if p == False:
			print("WARNING:%s is not installed."% i)
		programs[i] = p
	#発表順番
	playlist_file = d_root+"/playlist.csv"
	playlist = []
	if os.path.isfile(playlist_file):
		fp = open(playlist_file, "r", encoding="utf-8")
		for i in fp.readlines():
			l = i.strip().split(",")
			for i in range(len(l)):
				if l[i].startswith('"'):
					l[i] = l[i][1:]
				if l[i].endswith('"'):
					l[i] = l[i][:len(l[i])-1]
				l[i] = l[i].strip()
			if l != []:
				playlist.append(l)
		fp.close()
	else:
		print("ERROR:%s is not found."% playlist_file)
	for l in playlist:
		f = d_root+"\\"+l[0].strip()
		n = l[1].strip()
		c = [f]
		if f.endswith(".mp4"):
			c = [programs["vlc"], "--fullscreen", "--play-and-exit", f]
		elif f.endswith(".ppt") or f.endswith(".pptx") or f.endswith("pptsx"):
			c = [programs["powerpoint"], "/s", f]
		elif f.endswith(".odp"):
			c = [programs["libreoffice"], "--show", "--norestore", "--nodefault", f]
		cmds.append([f, c, n])
	return cmds

if __name__ == "__main__":
	cmds = load(d_root)
	for i in cmds:
		input(i[2]+"(Enter)")
		play(i[0],i[1])
