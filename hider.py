from PIL import Image, ImageTk
import tkinter as tk
from tkinter.filedialog import askopenfilename,askdirectory
import pickle

class popupDirWindow():
    def __init__(self,master,img):
        self.img=img
        top=self.top=tk.Toplevel(master)
        top.title("Dialogue")
        self.f1=tk.Frame(top)
        self.f2=tk.Frame(top)
        self.f1.pack()
        self.f2.pack()
        self.l1=tk.Label(self.f1,text="Chose an name:")
        self.l1.pack(side=tk.LEFT)
        self.e1=tk.Entry(self.f1)
        self.e1.insert(0,"img")
        self.e1.pack(side=tk.LEFT)
        self.l2=tk.Label(self.f2,text="Chose a location:")
        self.l2.pack(side=tk.LEFT)
        self.e2=tk.Entry(self.f2)
        self.e2.insert(0,"./")
        self.e2.pack(side=tk.LEFT)
        self.but=tk.Button(self.f2,command=self.getfile,text="Select")
        self.but.pack(side=tk.LEFT)
        self.b=tk.Button(top,text='Ok',command=self.cleanup)
        self.b.pack()
    def getfile(self):
        n=askdirectory()
        self.e2.delete(0,tk.END)
        self.e2.insert(0,n)
    def cleanup(self):
        self.name=self.e1.get()
        self.path=self.e2.get()
        path=self.path+self.name+".png"
        self.img.save(path,format="PNG")
        self.top.destroy()

class popupWindow():
    def __init__(self,master):
        top=self.top=tk.Toplevel(master)
        top.title("Dialogue")
        self.f1=tk.Frame(top)
        self.f2=tk.Frame(top)
        self.f1.pack()
        self.f2.pack()
        self.l1=tk.Label(self.f1,text="Chose an name:")
        self.l1.pack(side=tk.LEFT)
        self.e1=tk.Entry(self.f1)
        self.e1.insert(0,"img")
        self.e1.pack(side=tk.LEFT)
        self.l2=tk.Label(self.f2,text="Chose a image:")
        self.l2.pack(side=tk.LEFT)
        self.e2=tk.Entry(self.f2)
        self.e2.insert(0,"./imgs/default.jpg")
        self.e2.pack(side=tk.LEFT)
        self.but=tk.Button(self.f2,command=self.getfile,text="Search")
        self.but.pack(side=tk.LEFT)
        self.b=tk.Button(top,text='Ok',command=self.cleanup)
        self.b.pack()
        
    def getfile(self):
        n=askopenfilename()
        self.e2.delete(0,tk.END)
        self.e2.insert(0,n)
        
    def cleanup(self):
        self.name=self.e1.get()
        self.img=self.e2.get()
        self.top.destroy()

class mainWin():
    def __init__(self,master,im,usrid,gmid,openim=True):
        self.lists = {
        "upxy":[0,0],
        "downxy":[0,0],
        "movexy":[0,0]
        }
        self.name=""
        self.master=master
        self.root=tk.Frame(self.master)
        self.root.pack(fill=tk.X,)
        self.root2=tk.Frame(self.root)
        self.root2.pack()
        self.root3=tk.Frame(self.root)
        self.root3.pack()
        self.usrid=usrid
        self.gmid=gmid
        self.hidealpha=255
        if openim:
            self.img = Image.open(im)
            self.img = self.img.convert("RGBA")
        else:
            self.img=im
        self.x,self.y=self.minMaxWiHi(self.img.size)
        self.imgwidth, self.imgheight = self.img.size
        self.fowgen=Image.new("RGBA",(self.x,self.y),(0,0,0,self.hidealpha))
        #self.fowgen.putpixel((50,50),(0,255,0,255))
        self.fow=ImageTk.PhotoImage(self.fowgen)
        self.tkimage = ImageTk.PhotoImage(self.img)
        #canvas
        self.can = tk.Canvas(self.root, width=self.imgwidth, height=self.imgheight)
        self.can.bind("<Button-1>", lambda z: self.addxy(z.x,z.y,"downxy"))
        self.can.bind("<B1-Motion>", lambda z: self.addxy(z.x,z.y,"movexy"))
        self.can.bind("<ButtonRelease-1>", lambda z: self.addxy(z.x,z.y,"upxy"))
        self.can.pack()
        #add img and lines/box
        self.can.create_image(0,0, image=self.tkimage, anchor=tk.NW, )
        self.fowim=self.can.create_image(0,0, image=self.fow, anchor=tk.NW, )
        self.i1 = self.can.create_line(0,0,self.imgwidth,self.imgheight, fill="red")
        self.i2 = self.can.create_line(0,self.imgheight,self.imgwidth,0, fill="red")
        self.box = self.can.create_rectangle(0,0,0,0, outline="red")
        #gm buttons
        self.b1=tk.Button(self.root2, text="Hide All", command=lambda: self.clr(0,0,self.imgwidth,self.imgheight,self.hidealpha))
        self.b1.pack(side=tk.LEFT)
        self.b2=tk.Button(self.root2, text="Clear All", command=lambda: self.clr(0,0,self.imgwidth,self.imgheight))
        self.b2.pack(side=tk.LEFT)
        self.hidetoggle=tk.IntVar()
        self.linetoggle=tk.IntVar()
        self.screentoggle=tk.IntVar()
        self.c1 = tk.Checkbutton(self.root3, text="Conceal", variable=self.hidetoggle,offvalue=0, onvalue=1)
        self.c1.pack(side=tk.LEFT)
        self.c3 = tk.Checkbutton(self.root3, text="GM View", variable=self.screentoggle,offvalue=255, onvalue=155, command=self.hac)
        self.c3.toggle()
        self.c3.toggle()
        self.c3.pack(side=tk.LEFT)
        #user buttons
        self.c2 = tk.Checkbutton(self.root3, text="Centration lines", variable=self.linetoggle,offvalue=0, onvalue=1, command=self.linehide)
        self.c2.toggle()
        self.c2.invoke()
        self.c2.pack(side=tk.LEFT)
        #id check
        if self.usrid != self.gmid:
            self.c3.config(state=tk.DISABLED)
            self.c1.config(state=tk.DISABLED)
            self.b1.config(state=tk.DISABLED)
            self.b2.config(state=tk.DISABLED)
        else:
            self.c3.invoke()

    def addxy(self,x,y,type):
        if self.usrid != self.gmid:
            return
        self.lists[type][0]=x
        self.lists[type][1]=y
        if type == "downxy":
            self.can.itemconfig(self.box,state="normal")
        if type == "movexy":
            self.movebox(self.lists["downxy"][0],self.lists["downxy"][1],x,y)
        if type == "upxy":
            z=0
            if self.hidetoggle.get()==1:
                z=self.hidealpha
            self.clr(self.lists["downxy"][0],self.lists["downxy"][1],x,y,z)
            self.can.itemconfig(self.box,state="hidden")
            self.movebox(0,0,0,0)
    
    def kill(self):
        self.root.destroy()
        self.root2.destroy()
        self.root3.destroy()
        self.can.destroy()
        self.b1.destroy()
        self.b2.destroy()
        self.c1.destroy()
        self.c3.destroy()
        self.c2.destroy()

    def minMaxWiHi(self,size): #change img size
        imghi,imgwi=size
        minhi=50
        minwi=50
        maxwi=700
        maxhi=500
        if imgwi < minwi or imghi < minhi:
            self.img.thumbnail((minwi,minhi),Image.ANTIALIAS)
        if imgwi > maxwi or imghi > maxhi:
            self.img.thumbnail((maxwi,maxhi),Image.ANTIALIAS)
        return self.img.size

    def clr(self,x1,y1,x2,y2,alpha=0):
        x3=x1
        x4=x2
        y3=y1
        y4=y2
        if x2 < x1:
            x3=x2
            x4=x1
        if y2 < y1:
            y3=y2
            y4=y1
        if y3 < 0:
            y3=0
        if y4 > self.imgheight:
            y4=self.imgheight
        if x3 < 0:
            x3=0
        if x4 > self.imgwidth:
            x4=self.imgwidth
        #print("x's: %i,%i\ny's: %i,%i"%(x3,x4,y3,y4))
        for x in range(x3,x4):
            for y in range(y3,y4):
                self.fowgen.putpixel((x,y),(0,0,0,alpha))
        self.fow=ImageTk.PhotoImage(self.fowgen)
        self.can.itemconfig(self.fowim, image=self.fow)
        
    def movebox(self,x1,y1,x2,y2):
        self.can.coords(self.box,(x1,y1,x2,y2))
    
    def linehide(self):
        z=tk.HIDDEN
        if self.linetoggle.get()==1:
            z=tk.NORMAL
        self.can.itemconfig(self.i1,state=z)
        self.can.itemconfig(self.i2,state=z)

    def hac(self):
        self.hidealpha=self.screentoggle.get()
        for x in range(0,self.imgwidth):
            for y in range(0,self.imgheight):
                if self.fowgen.getpixel((x,y)) != (0,0,0,0):
                    self.fowgen.putpixel((x,y),(0,0,0,self.hidealpha))
        self.fow=ImageTk.PhotoImage(self.fowgen)
        self.can.itemconfig(self.fowim, image=self.fow)

    def setFowgen(self,gen):
        self.fowgen=gen
        self.hac()
        
class room():
    def __init__(self,root,usrid=0,gmid=0):
        self.gmid=gmid
        self.usrid=usrid
        self.imindex=0
        self.buttonwidth=80
        self.btswds=[]
        self.selectedL=tk.Label(root,text="Displaying: None")
        self.btspack=True
        self.top=root
        self.root=tk.Frame(self.top)
        self.root.pack()
        self.f=tk.Frame(self.root)
        self.f.pack(fill=tk.X)
        self.clbut=tk.Button(root,text="Delete tab",command=self.destruct)
        self.selectedL.pack()
        self.clbut.pack()
        self.wins=[]
        self.bts=[]
        self.mbts=[]
        self.but=tk.Button(self.f,text="+",command=self.newIm)
        self.but.pack(side=tk.LEFT)
        #menu
        self.mb=tk.Menubutton(self.f, text="Menu", relief=tk.RAISED)
        self.mb.menu=tk.Menu(self.mb, tearoff = 0)
        self.mb["menu"] =  self.mb.menu
        self.mb.menu.add_command(label="Save",command=self.save)
        self.mb.menu.add_command(label="Load",command=self.load)
        self.mb.menu.add_command(label="Export image",command=self.exportimg)
        self.mb.menu.add_command(label="Leave room",command=self.lvroom,state=tk.DISABLED)
        self.mb.menu.add_command(label="Exit program",command=lambda:exit())
        self.mb.pack(side=tk.RIGHT)
        #mb2
        self.mb2=tk.Menubutton(self.f, text="Active tabs", relief=tk.RAISED)
        self.mb2.menu=tk.Menu(self.mb2, tearoff = 0)
        self.mb2["menu"] =  self.mb2.menu

    def save(self):
        #print("saving..")
        win={}
        m=0
        for i in self.wins:
            fowgen=[[0]*i.imgheight for n in range(i.imgwidth)]
            img=[[0]*i.imgheight for n in range(i.imgwidth)]
            for x in range(0,i.imgwidth):
                for y in range(0,i.imgheight):
                    fowgen[x][y]=i.fowgen.getpixel((x,y))
                    img[x][y]=i.img.getpixel((x,y))
            win["win"+str(m)]={}
            win["win"+str(m)]["fowgen"]=fowgen
            win["win"+str(m)]["img"]=img
            win["win"+str(m)]["w"]=i.imgwidth
            win["win"+str(m)]["h"]=i.imgheight
            win["win"+str(m)]["name"]=i.name
            m+=1
        obj=saveit(win,self.gmid)
        with open("save.txt","wb") as file:
            pickle.dump(obj,file,3)
        #print("%s\n%s\n%s\n%s"%(str(win),str(self.buttonwidth),str(self.imindex),str(self.gmid)), file=open("save.txt","w"))

    def load(self,client=True):
        ind=len(self.wins)
        for i in range(ind):
            self.destruct()
        with open("save.txt","rb") as file:
            loaded=pickle.load(file)
        win = loaded.wins
        self.gmid=loaded.gmid
        if client:
            self.usrid=self.gmid
        ind=0
        for w in win:
            #print("%i\n%i\n%s"%(win[w]["w"],win[w]["h"],win[w]["name"]))
            ne=Image.new("RGBA",(win[w]["w"],win[w]["h"]),(0,0,0,255))
            for x in range(win[w]["w"]):
                for y in range(win[w]["h"]):
                    ne.putpixel((x,y),win[w]["img"][x][y])
            nm=Image.new("RGBA",(win[w]["w"],win[w]["h"]),(0,0,0,255))
            for x in range(win[w]["w"]):
                for y in range(win[w]["h"]):
                    nm.putpixel((x,y),win[w]["fowgen"][x][y])
            self.loadnewIm(ne,win[w]["name"])
            #print(ind)
            #print(self.wins[ind])
            #print(self.wins)
            self.wins[ind].setFowgen(nm)
            ind+=1

    def destruct(self):
        x=self.imindex
        self.wins[x].kill()
        self.bts[x].destroy()
        self.mb2.menu.delete(x)
        self.buttonwidth-=self.btswds[x]
        del self.btswds[x]
        del self.wins[x]
        del self.bts[x]
        z=len(self.wins)-1
        num=0
        for x in range(z+1):
            self.fixbtns(x)
        if z>=0:
            self.shwin(z)
        else:
            self.selectedL.config(text="Displaying: None")

    def fixbtns(self,x):
        self.bts[x].config(command=lambda:self.shwin(x))

    def lvroom(self):
        pass

    def exportimg(self):
        im1=self.wins[self.imindex].img
        im2=self.wins[self.imindex].fowgen
        n=Image.alpha_composite(im1, im2)
        popupDirWindow(self.top,n)

    def frmWth(self,index):
        self.wins[index].root.update()
        z=self.wins[index].root.winfo_width()
        #print("x: %i\nz: %i"%(self.buttonwidth,z))
        if self.buttonwidth > z: 
            if self.btspack==True:
                for i in self.bts:
                    i.pack_forget()
                self.mb2.pack(side=tk.LEFT)
                self.btspack=False
        else:
            if self.btspack==False:
                for i in self.bts:
                    i.pack(side=tk.LEFT)
                self.mb2.pack_forget()
                self.btspack=True
        self.but.pack_forget()
        self.but.pack(side=tk.LEFT)

    def loadnewIm(self,img,name):
        c=len(self.bts)
        self.wins.append(mainWin(self.root,img,self.usrid,self.gmid,False))
        self.bts.append(tk.Button(self.f,text=name,command=lambda:self.shwin(c)))
        self.mbts.append(self.mb2.menu.add_command(label=name,command=lambda:self.shwin(c)))
        self.bts[c].pack(side=tk.LEFT)
        self.bts[c].update()
        z=self.bts[c].winfo_width()
        if self.btspack==False:
            self.bts[c].pack_forget()
        self.btswds.append(z)
        self.buttonwidth+=z
        self.wins[c].name=name
        self.shwin(c)

    def newIm(self):
        c=len(self.bts)
        n=popupWindow(self.top)
        self.but["state"] = "disabled" 
        self.root.wait_window(n.top)
        self.but["state"] = "normal"
        if not hasattr(n,"name"):
            return
        self.wins.append(mainWin(self.root,n.img,self.usrid,self.gmid))
        self.bts.append(tk.Button(self.f,text=n.name,command=lambda:self.shwin(c)))
        self.mbts.append(self.mb2.menu.add_command(label=n.name,command=lambda:self.shwin(c)))
        self.bts[c].pack(side=tk.LEFT)
        self.bts[c].update()
        z=self.bts[c].winfo_width()
        if self.btspack==False:
            self.bts[c].pack_forget()
        self.btswds.append(z)
        self.buttonwidth+=z
        self.wins[c].name=n.name
        self.shwin(c)

    def shwin(self,index):
        #print(index)
        #make sure imindex is not out of range
        if self.imindex < len(self.wins): 
            self.wins[self.imindex].root.pack_forget()
        self.wins[index].root.pack(side=tk.LEFT) 
        self.imindex=index
        self.selectedL.config(text="Displaying: "+self.wins[index].name)
        self.frmWth(index)

class saveit():
    def __init__(self,win,gmid=0):
        self.wins=win
        self.gmid=gmid

if __name__ == '__main__':
    root = tk.Tk()
    root.resizable(0,0)
    root.title("MapHider")
    rom=room(root)
    rom.newIm()
    root.mainloop() 