import tkinter as tk
from tkinter import filedialog
import pickle
class notebook(object):
	"""docstring for notebook"""
	def __init__(self):
		self.file_opened=0
		self.root=tk.Tk()
		try:
			with open("Notebook.cache","rb") as f:
				self.openedfile=pickle.load(f)
				self.explorer_open=pickle.load(f)
		except:
			self.openedfile=None
			self.explorer_open=False
		if self.explorer_open:
			if self.openedfile !=None:
				self.explorer()
		else:
			self.explorer_open=True

		menu=tk.Menu(self.root)
		self.root.config(menu=menu)
		self.root.bind("<Control-s>",self.save_file)
		self.root.bind("<Control-S>",self.save_as_file)
		self.root.bind("<Control-o>",self.open_file)
		self.root.bind("<Control-e>",self.explorer)
		File=tk.Menu(menu)
		View=tk.Menu(menu)
		File.add_command(label="New")
		File.add_command(label="Open ctrl+o",command=self.open_file)
		File.add_command(label="Save ctrl+s",command=self.save_file)
		File.add_command(label="Save As ctr+shiftl+S",command=self.save_as_file)
		View.add_command(label="Show the explorer ctrl+e",command=self.explorer)
		menu.add_cascade(label="File",menu=File)
		menu.add_cascade(label="View",menu=View)
		self.text=tk.Text(self.root)
		self.text.pack(side="right")
		if self.openedfile !=None:
			with open(self.openedfile) as f:
				self.root.title(self.openedfile)
				self.text.insert(1.0,f.read())

		self.root.mainloop()
		with open("Notebook.cache","wb") as f:
			pickle.dump(self.openedfile,f)
			pickle.dump(not self.explorer_open,f)


	def open_file(self,event=None,openedfile=None):
		self.openedfile=filedialog.askopenfilename(initialdir="/")
		if len(self.openedfile)>1:
			with open(self.openedfile) as f:
				self.data=f.read()
			self.text.delete(1.0,tk.END)
			self.text.insert(1.0,self.data)
			self.root.title(self.openedfile)
			self.file_opened=1
	def save_as_file(self,event=None):
		a=filedialog.asksaveasfile()
		if a !=None:
			self.data=self.text.get(1.0,tk.END)
			a.write(self.data)
			a.close()
			self.root.title(a.name)
			self.openedfile=a.name
	def save_file(self,event=None):
		if self.file_opened:
			with open(self.openedfile,"w") as f:
				f.write(self.text.get(1.0,tk.END))
				self.root.title(self.openedfile)
		else:
			self.save_as_file()

	def explorer(self,event=None):
		if self.explorer_open:

			self.View_frame=tk.PanedWindow()
			self.View_frame.pack(side="left",padx=10,fill="y",expand=1,anchor='nw')
			from os import listdir
			openedfile=self.openedfile.replace("/","\\")
			openedfile=openedfile.split("\\")
			openedfile.pop(-1)
			opendir=openedfile
			directory=''
			for i in opendir:
				directory=directory+i+"\\"
			for i,file in enumerate(listdir(directory)):
				if not ".mp4" in file:
					self.l=tk.Label(self.View_frame,text=file)
					self.l.grid(row=i,column=0)
		if not self.explorer_open:
			self.View_frame.destroy()
		self.explorer_open=not self.explorer_open

notebook()
