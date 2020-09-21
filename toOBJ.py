from to3D import *
from myColors import *
def toStr(v):
    return str(v[0])+" "+str(v[1])+" "+str(v[2])

def getMaterial(name):
    if name == "earth":
        return getEarthColor()
    if name == "road":
        return getRoadColor()
    if name == "field":
        return getFieldColor()
    if name == "planks":
        return getPlanksColor()
    if name == "greens":
        return getGreensColor()
    if name == "rivers":
        return getRiversColor()
    if name == "citywall":
        return getCityWallColor()
    if name == "citytower":
        return getCityTowerColor()
    if name == "wallb": # building walls, NOT city walls
        return getWallbColor()
    if name == "roof":
        return getRoofColor()
    if name == "square":
        return getSquareColor()
    if name == "prisms":
        return getPrismsColor()
    
def writeMTL(objs, file, name):
    '''
    write the material file for all the objects in objs
    '''
    for i in range(len(objs)):
        il, kd, ks, ka, tf, ns, ni=getMaterial(name)
        file.write("newmtl "+name+"_"+str(i)+"\n")
        file.write("\t illum "+str(il)+"\n")
        file.write("\t Kd "+toStr(kd)+"\n")
        file.write("\t Ks "+toStr(ks)+"\n")
        file.write("\t Ka "+toStr(ka)+"\n")
        file.write("\t Tf "+toStr(tf)+"\n")
        file.write("\t Ns "+str(ns)+"\n")
        file.write("\t Ni "+str(ni)+"\n")

def writeObjects(objs, file, c, name):
    
    file.write("g "+name+"\n")
    i=0
    for o in objs:#there is one normal per triangle, so it's ok
        file.write("o "+name+"_"+str(i)+"\n")
        file.write("usemtl "+name+"_"+str(i)+"\n")
        writeFaces(len(o), c, file)
        i+=1
        c+=len(o)*3
        
    return c

def writeFaces(n, i, file):
    #i=currentCount, n lenght of this one
    #one line per triangle
    for id in range(n):
        file.write("f ")
        step=i+3*id
        file.write(str(step)+"//"+str(int((step+2)/3))+" ")
        
        file.write(str(step+1)+"//"+str(int((step+2)/3))+" ")
        
        file.write(str(step+2)+"//"+str(int((step+2)/3))+"\n")
        
    
def writeTriangleArray(array, file):
    '''
    writes in the file the array of triangles
    '''
    for a in array:
        for t in a:
            file.write(vertex(t, False))
        
def writeNormalArray(array, file):
    '''
    writes in the file the array of vertices
    '''
    for a in array:
        file.write(vertex(a, True))
        
def vertex(v, n=False):
    x, z, y=v
    s=""
    if(n):
        s="vn "
    else:
        s="v "

    s+=str(x)+" "+str(y)+" "+str(z)+"\n"
    return s