# サークル紹介スライドランチャー GUI
#nuitka --mingw64 --follow-imports --standalone --onefile --windows-console-mode=disable --enable-plugin=tk-inter --windows-icon-from-ico="favicon.ico" play_slides_control.py
import tkinter
import os
import play_slides
d_root = play_slides.d_root
TITLE = "新入生ガイダンス サークル紹介"
BG = "#fff"
FC = "#111"
class SlideCtl:
	__slots__ = ("root","title","play_btn","start")
	def __init__(self):
		root = tkinter.Tk()
		root.attributes("-fullscreen", True)
		root.config(bg=BG)
		root.title(TITLE)
		self.start = 0
		i = play_slides.d_root+"/favicon.ico"
		if os.path.isfile(i):
			try:
				root.iconbitmap(default=i)
			except:
				pass
		self.title = tkinter.Label(root,text=TITLE,bg=BG,fg="#0cf",anchor="w",font=("",32))
		dsc = tkinter.Label(root,text="一度再生すると、途中で停止出来ません。\nEscキーで閉じます。",bg=BG,fg=FC,font=("",24))
		self.play_btn = tkinter.Button(root,text="Play",font=("",24),command=self.play)
		self.title.place(x=10,y=10)
		dsc.place(x=20,y=60)
		self.play_btn.grid(row=0, column=0, sticky="")
		root.grid_rowconfigure(0, weight=1)
		root.grid_columnconfigure(0, weight=1)
		self.root = root
		self.root.bind("<Return>", self.play)
		self.root.bind("<Escape>", self.exit)
		self.root.mainloop()
	def play(self, a=None):
		play_slides.play_from(self.start)
		self.exit()
	def exit(self, a=None):
		self.root.quit()
if __name__ == "__main__":
	SlideCtl()

