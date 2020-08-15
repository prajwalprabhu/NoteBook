import os
import tkinter as tk
from tkinter import EXCEPTION, filedialog,messagebox
from json import load,dump
from threading import Thread, active_count, current_thread
from time import sleep
class notebook(object):
	
	"""docstring for notebook"""
	def __init__(self):
		self.file_opened=False
		self.app=True
		self.root=tk.Tk()
		self.load_data()
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
		self.root.bind("<Control-n>",self.new_file)
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
		self.text.grid(row=0,column=2)
		self.text.configure(height=42)
		if self.openedfile !=None and len(self.openedfile)>4:
			self.open_file(file=self.openedfile)
		self.thread=Thread(target=self.collect_data)
		self.thread.start()
		self.root.mainloop()
		self.app=False
		self.check()
		self.dump_data()
		self.ask_exit()

		

	def open_file(self,event=None,file=None):
		self.lastopenedfile=self.openedfile
		if file==None:
			self.openedfile=filedialog.askopenfilename(initialdir="/")
		else:
			self.openedfile=file
		if os.path.isdir(self.openedfile):
			self.list_dir(file=self.openedfile)
			pass
		elif  os.path.isfile(self.openedfile):
			with open(self.openedfile) as f:
				self.data=f.read()
			self.text.delete(1.0,tk.END)
			self.text.insert(1.0,self.data)
			self.root.title(self.openedfile)
			self.file_opened=True
			if not self.explorer_open:
				self.explorer()
				self.explorer()
		else:
			messagebox.showerror("No File Opened","No File is Selected to open")
	def save_as_file(self,event=None):
		a=filedialog.asksaveasfile()
		if a !=None:
			a.write(self.page_data)
			a.close()
			if self.app:
				self.root.title(a.name)
			self.openedfile=a.name
	def save_file(self,event=None):
		if os.path.isfile(self.openedfile):
			with open(self.openedfile,"w") as f:
				f.write(self.page_data)
				self.root.title(self.openedfile)
		else:
			self.save_as_file()

	def explorer(self,event=None):
		if self.explorer_open and len(self.openedfile)>=4:
			sframe=tk.Frame(self.root)
			sframe.grid(row=0,column=1)
			sb=tk.Scrollbar(sframe,orient="vertical")
			sb.pack(fill="y")
			self.list=tk.Listbox(self.root,yscrollcommand=sb.set)
			self.list.grid(row=0,column=0)
			self.list.configure(height=43)
			sb.config(command=self.list.yview)
			self.list_dir()
			
		if not self.explorer_open:
			self.list.destroy()
		self.explorer_open=not self.explorer_open

	def new_file(self,event=None):

		if len(self.openedfile)>5:
			if os.path.isfile(self.openedfile):
				with open(self.openedfile) as f:
					data=f.read()
				text=self.page_data
				self.asddir,name=os.path.split(self.openedfile)
				if not text==data:
					choice=messagebox.askyesno("File not saved","Doyou want to save the file")
					if choice:
						self.save_file()
		else:
			self.asddir=os.getcwd()
		self.root.title(os.path.normcase(f"{self.asddir}//Untitled-1.txt"))
		self.lastopenedfile=self.openedfile
		self.openedfile=os.path.normcase(os.path.join(self.asddir,"Untitled-1.txt"))
		try:
			self.text.delete(1.0,tk.END)
		except AttributeError:
			pass
	
	def check(self):
		if not os.path.isfile(self.openedfile):
			choice=messagebox.askyesno("File not saved","Doyou want to save the file")
			if choice:
				self.save_file()
				print("if")
			else:
				self.openedfile=self.lastopenedfile
				print("else")
	def dump_data(self):
		try:
			with open(os.getcwd()+"\\data\\Note_Book_data.json","w") as f:
				self.json_data["path"]=self.openedfile
				self.json_data["explorer"]=not self.explorer_open
				dump(self.json_data,f,indent=4,sort_keys=True)
		except AttributeError:
			pass
	def collect_data(self):
		print("collecting data")
		try:
			while 1:
				if self.app==True:
					self.page_data=self.text.get(1.0,tk.END)
				else:
					break
		except Exception as e:
			return None
						
	def load_data(self):
		try:
			with open(os.getcwd()+"\\data\\Note_Book_data.json","r") as f:
				self.json_data=load(f)
				self.openedfile=self.json_data["path"]
				self.explorer_open=self.json_data["explorer"]
		except Exception as e:
			self.openedfile=None
			self.explorer_open=False
	def ask_exit(self):
		a=messagebox.askyesno("Exit","Do You Wnat to exit")
		if not a:
			notebook()
	def double_click(self,event=None):
		file=self.list.get("anchor")
		file_temp=list(file)
		if "folder" in file:
			print("folder found")
			for _ in range(0,9):
				file_temp.pop(0)
			file=''
			for i in range(0,len(file_temp)):
				file=file+file_temp[i]
				pass

		
		if os.path.isfile(self.openedfile):
			dir,_=os.path.split(self.openedfile)
		else:
			dir=self.openedfile
		file_temp=os.path.normcase(os.path.join(dir,file))
		print(file_temp)
		self.open_file(file=file_temp)

	def list_dir(self,file=None):
		if file==None:
			dir,file = os.path.split(self.openedfile)
		else:
			dir=file
		self.list.delete(0,tk.END)
		for i,file in enumerate(os.listdir(dir)):
			if not ".mp4" in file:
				

				if  os.path.isdir(os.path.join(dir,file)):
					self.list.insert("end",f"folder \t {file}")
				else:
					# print("else encontered")
					self.list.insert("end",file)
		self.list.bind("<Button-1>",self.double_click)
	def sleepp(self,t):
		sleep(t)
		notebook()

notebook()















