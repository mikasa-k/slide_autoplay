# サークル紹介スライドランチャー GUI
#nuitka --mingw64 --follow-imports --standalone --onefile --windows-console-mode=disable --enable-plugin=tk-inter --windows-icon-from-ico="favicon.ico" main.py
import tkinter
import os
import threading
import play_slides
d_root = play_slides.d_root
TITLE = "新入生ガイダンス サークル紹介"
BG = "#eff"
FC = "#111"
class SlideCtl:
	__slots__ = ("root","title","next_title","dsc","play_btn","back_btn","cmds","start","thread","wait","is_wait")
	def __init__(self):
		root = tkinter.Tk()
		root.attributes("-fullscreen", True)
		root.config(bg=BG)
		root.title(TITLE)
		self.start = 0
		self.wait = 10
		self.is_wait = True
		self.thread = None
		self.cmds = play_slides.load(d_root)
		i = d_root+"/favicon.ico"
		if os.path.isfile(i):
			try:
				root.iconbitmap(default=i)
			except:
				pass
		width = root.winfo_screenwidth()
		height = root.winfo_screenheight()
		self.title = tkinter.Label(root,text=TITLE,bg=BG,fg="#0af",anchor="w",font=("",40))
		self.next_title = tkinter.Label(root,bg=BG,fg="#0af",anchor="w",font=("",28))
		self.dsc = tkinter.Label(root,text="ボタンを押して開始します",bg=BG,fg=FC,font=("",24))
		self.play_btn = tkinter.Button(root,text="スタート",font=("",24),command=self.play)
		self.back_btn = tkinter.Button(root,text="Redo",font=("",24),command=self.replay)
		writer_file = "writer.txt"
		if os.path.isfile(writer_file):
			writer = tkinter.Label(root,bg=BG,fg=FC,font=("Arial",18))
			writer.place(x=10,y=height//2+100)
			with open(writer_file,"r",encoding="utf-8") as fp:
				writer.config(text=fp.read())
		self.title.place(x=10,y=10)
		self.dsc.place(x=20,y=70)
		self.next_title.place(x=15,y=height-80)
		self.play_btn.place(x=width//2-150,y=height//2)
		self.back_btn.place(x=width//2+50,y=height//2)
		if self.cmds == []:
			self.next_title.config(text="再生するものがありません")
		else:
			self.next_title.config(text="次は、"+self.cmds[self.start][2]+" "+self.cmds[self.start][0].replace(d_root+"\\",""))
		self.increment_wait()
		self.root = root
		self.root.bind("<Return>", self.play)
		self.root.bind("<Control-Key-q>", self.exit)
		self.root.mainloop()
	def play(self, a=None):
		if self.wait < 3:
			self.dsc.config(text="3秒以上時間を置いてからボタンを押してください。")
			if self.is_wait:
				self.dsc.after(1000*(3-self.wait), self.play)
				self.is_wait = False
			return
		if (self.thread and self.thread.is_alive()) or play_slides.is_wait:
			self.dsc.config(text="ファイルが閉じるのを待っています...")
			self.dsc.after(1000, self.play)
			return
		self.wait = 0
		self.is_wait = True
		if self.start < len(self.cmds):
			self.play_btn.config(text="次　へ")
			i = self.cmds[self.start]
			self.dsc.config(text=i[0].replace(d_root+"\\",""))
			self.title.config(text=i[2])
			self.thread = threading.Thread(target=play_slides.play, args=(i[0],i[1]))
			self.thread.start()
			self.start += 1
			if self.start < len(self.cmds):
				self.next_title.config(text="次は、"+self.cmds[self.start][2]+" "+self.cmds[self.start][0].replace(d_root+"\\",""))
			else:
				self.next_title.config(text="終了です。")
		else:
			self.start = 0
			self.title.config(text=TITLE)
			self.dsc.config(text="全て再生し終えました。お疲れ様です。(Ctrl+Qで終了)")
			self.play_btn.config(text="もう一度")
	def replay(self):
		self.start = max(0, self.start-1)
		self.play()
	def increment_wait(self):
		self.wait += 1
		self.play_btn.after(1000, self.increment_wait)
	def exit(self, a=None):
		self.root.quit()
if __name__ == "__main__":
	SlideCtl()

