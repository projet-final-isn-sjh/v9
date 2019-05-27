import tkinter as tk
from math import cos,sin,pi

shapes=([0,0,1,1],
        [0,0,40,0,40,40,0,40],
        [0,40,20,6,40,40],
        [0,0,40,0,40,20,0,20],
        [0,0,20,34,40,0],
        [0,40,5,10,10,40,15,0,20,30,25,0,30,40,35,10,40,40],
        [-15,0,15,0,15,-30,-15,-30]) #cube

        
def rotation(points,center=(0,0),angle=0): #angle radian
    xo,yo=center
    rotate_points=tuple()
    for i in range(len(points)//2):
        x,y=points[2*i],points[2*i+1]
        x1,y1=x-xo,y-yo
        rotate_points+=(int(x1*cos(angle)+y1*sin(angle)+xo),int(y1*cos(angle)-x1*sin(angle)+yo))
    return rotate_points

side=lambda points:len(points)//2
absciss=lambda points:[points[2*i] for i in range(side(points))]
ordinate=lambda points:[points[2*i+1] for i in range(side(points))]



def shape(shape_properties):
    n_shape,yo,xo=shape_properties
    points=shapes[n_shape]
    m=side(points)
    x=absciss(points)
    y=ordinate(points)
    points=tuple()
    for i in range(m):
        points+=(x[i]+xo,y[i]+yo)
    return points

def percent(counter,lenght):
    return str(int(counter/lenght*100))+"%"
    
    
def decode(data):
    data+="\n0-0"*15
    texture=list()
    lines=data.split("\n")
    for line in lines:
        instructions=line.split("+")
        l=len(instructions)
        for i in range(l):
            instruction=instructions[i].split("-")
            if int(instruction[0]):
                texture.append((int(instruction[0]),int(instruction[1]),760+i*step))
            else:
                texture.append((0,0,0))
        for i in range(10-l):
            texture.append((0,0,0))
    return texture
    
class Display:
    def __init__(self,canvas):
        self.canvas=canvas

    def create(self,instruction):
        self.canvas.create_polygon(shape(instruction),fill="purple",outline="white",width=2)

    def init(self,nb):
        for i in range(nb):
            self.canvas.create_polygon(0,0,1,1,fill="purple",outline="white",width=2)

    def replace(self,instruction,item,tag):
        self.canvas.coords(item,shape(instruction))
        self.canvas.itemconfig(item,tag=tag)

    def Get_item(self,x1,y1,x2,y2):
        items=self.canvas.find_overlapping(x1,y1,x2,y2)
        if items:
            return items[-1]
        else:
            return 0

    def Get_item_sensor(self,item,difference=0):
        coords=self.canvas.coords(item)
        coords+=(coords[0],coords[1])
        sensor=list()
        for i in range(len(coords)//2-1):
            result=self.Get_item(coords[2*i],coords[2*i+1]+difference,coords[2*i+2],coords[2*i+3]+difference)
            if result!=item:
                sensor.append(result)
            else:
                sensor.append(None)
        return sensor
            

class Game:
    def __init__(self):
        clean(root)
        self.height={1:0,2:400}
        #decode map
        file=open("map.txt","r")
        data=file.read()
        file.close()
        self.data=decode(data)
        self.lenght=len(self.data)-1
        
        self.canvas=tk.Canvas(root,width=800,height=450,bg=color[0])
        self.canvas.pack()
        self.cube=self.canvas.create_polygon(shape((6,400,200)),fill=color[1],outline=color[2],width=5)
        self.canvas.create_polygon(0,400,800,400,800,450,0,450,fill=color[3],width=3,outline=color[4])
        self.canvas.create_text(400,430,tag="text",font=("Arial","25"),fill="white")
        self.display=Display(self.canvas)
        self.display.init(80)
        self.counter=0
        self.lenght_jmp=25
        #Movement
        self.vy=0
        self.y=200
        self.jmp=False
        self.last_jmp=0
        self.disable_jmp=0
        root.bind("<space>",self.jump)
        #initialisation
        self.append()

    def append(self):
        self.canvas.coords(self.cube,rotation(shape((6,self.y-4,200)),center=(200,self.y-19),angle=-self.disable_jmp/25*pi))
        self.sensor=self.display.Get_item_sensor(self.cube,difference=5)

        self.canvas.move("map",step,0)
        destroy=self.canvas.find_overlapping(40,0,40,397) #return id of shapes which are on the line (d):x=40 
        if destroy:
            self.display.replace((0,0,0),destroy[0],'')
        available=self.canvas.find_overlapping(0,0,0,0)
        instruction=self.data[self.counter]
        if instruction[0] in [2,5]:
            self.height[available[0]]=450
        else:
            self.height[available[0]]=instruction[1]

        self.y-=int((3/5)*self.vy)
        self.vy-=1

        if self.sensor[0]:
            self.y=self.height[self.sensor[0]]
            self.vy=0

            if self.jmp:
                self.jmp=False
                self.last_jmp=self.counter
                self.vy=19
                self.y-=5
                
        self.disable_jmp=(self.counter-self.last_jmp)*(self.counter-self.last_jmp<self.lenght_jmp)
        death_sensor=self.sensor[2] and (self.sensor[1] or self.sensor[3]) or self.y==450


        self.display.replace(instruction,available[0],bool(instruction[0])*"map")
        self.canvas.itemconfig("text",text=percent(self.counter,self.lenght))
        self.counter+=1

        
        if self.counter!=self.lenght and not death_sensor:
            root.after(10,self.append)

    def jump(self,event):
        #Si on se trouve au delà du milieu du saut, alors le saut est autorisé
        if not self.disable_jmp:
            self.jmp=True

        
        
    

def clean(parent):
    for i in parent.winfo_children():
        i.destroy()
        
step=-4
root=tk.Tk()
color=["blue","red","pink","grey","white","purple","white"]
Game()
root.mainloop()

