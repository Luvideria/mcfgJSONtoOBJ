import numpy as np
import tripy

def normalFromSeg(p0, p1):
    '''
    p1, p2 : points of the segment
    Returns the normal (normalized) of the segment
    if the polygon is written in clockwise order, it's the correct (outer) normal.
    '''
    dx=p1[0]-p0[0]
    dy=p1[1]-p0[1]
    norm=np.sqrt(dx*dx+dy*dy)
    if norm==0:
        if dx==dy:
            print("you are trying to use normalFromSeg with two identical numbers")
            print("make sure you didn't try to close a contour twice!")
        else:
            print(f' norm: {norm:.2f}')
            print(f'dx,dy: {dx:.2f},{dy:.2f}')
            print(f'p0: {p0:.2f}')
            print(f'p1: {p1:.2f}')
            print("___")
    dx=dx/norm
    dy=dy/norm
    return [-dy, dx]

def contourFromLine(line,width=5):
    hw=width/2
    lower=list()
    higher=list()
    
    n=normalFromSeg(line[0], line[1])
    for i in range(len(line)):
        xi,yi=line[i]
        
        lower.append( [xi-n[0]*hw, yi-n[1]*hw] )
        higher.append( [xi+n[0]*hw, yi+n[1]*hw] )
        if not i==len(line)-1:
            n=normalFromSeg(line[i], line[i+1])
        
        
    line=higher+lower[::-1]
    line.append(line[0]) #closes the line
    return line

def contourFromRoad(road):
    return contourFromLine(road["coordinates"],road["width"])

def getRoads(roads):
    roadSurfaces=list()
    roadNormals=list()
    for r in roads:
        roadSurface, roadNormal=getSurface(getRoad(r), 0.1)
        roadSurfaces.append(roadSurface)
        roadNormals.append(roadNormal)
    
    return roadSurfaces, roadNormals

# make two lines displaced by width/2 from center


def getRoad(road, width=-1):
    '''
    road: dict where coordinates contain the line of points and width contains a positive number
    width: overrides the desired width of the road
    returns: closed loop of the shape of the road [[x, y], ...] can be fed to getSurface
    '''
    
    return contourFromRoad(road)

def getCityWalls(cityContour, height=10):
    '''
    field: a contour [[x, y], [x, y]]
    returns either a plane that has height just above the ground (0) or a surface with walls
    '''
    triangles=list()
    normals=list()
    for seg in cityContour:        
        if seg[0]==seg[-1]:
            seg=seg[0:-1]
        t, n=getCityWall(seg, height)
        triangles.append(t)
        normals.append(n)
    return triangles, normals

def getCityWall(cityWall, height=10):
    '''
    field: a contour [[x, y], [x, y]]
    returns either a plane that has height just above the ground (0) or a surface with walls
    '''
    triangles=list()
    normals=list()
    
    triangles, normals = getWalls(cityWall, height)
    
    top, ntop=getSurface(cityWall, height) #either we get them with {} or we leave it like that
    triangles.extend(top)
    normals.extend(ntop)
    return triangles, normals

def getField(field, height=0.1):
    '''
    field: a contour [[x, y], [x, y]]
    returns either a plane that has height just above the ground (0) or a surface with walls
    '''
    doWalls=False
    triangles=list()
    normals=list()
    field.append(field[0]) #to get a closed loop
    if not height==0.1:
        triangles, normals=getWalls(field, height)
    
    top, ntop=getSurface(field, height) #either we get them with {} or we leave it like that
    triangles.extend(top)
    normals.extend(ntop)
    return triangles, normals

def getFields(fields, height=0.1):
    triangles=list()
    normals=list()
    for f in fields:
        t, n=getField(f[0], height)
        triangles.append(t)
        normals.append(n)
    return triangles, normals

def getSurfaces(contours, height):
    triangles=list()
    normals=list()
    for c in contours:
        t, n=getSurface(c[0], height)
        triangles.append(t)
        normals.append(n)
    return triangles, normals

def getEarth(earth, height=0):
    return getSurface(earth, height)
    
def getSurface(contour, height):    
    surfacetris=tripy.earclip(contour)
    #this above returns something of the form ( ((1, 0), (0, 1), (0, 0)), ((...), ...), ... )
    #this below converts it to array( [ [1, 0, height], [0, 1, height], [0, 0, height] ], [[...], ...]... )
    surface = [np.array([np.append(a, [height]), np.append(b, [height]), np.append(c, [height])]) 
               for a, b, c in surfacetris]
    return surface, np.array([[0, 0, 1]]*len(surface))
    
def getWalls(contour, height):
    triangles=list()
    normals=list() #each triangle has exactly one norm    
    x, y=np.array(contour).transpose()
    x=np.append(x, [x[0]])
    y=np.append(y, [y[0]])
    z=np.array([0]*len(x))#assume ground is 0
    
    x0, y0, z0=[0, 0, 0]
    skip=True
    for xi, yi, zi in zip(x, y, z):
        if skip:
            x0, y0, z0=[xi, yi, zi]
            skip=False
            continue
        
        tri1 = np.array([[x0, y0, z0], [xi, yi, height], [xi, yi, zi]])
        tri2 = np.array([[x0, y0, z0], [x0, y0, height], [xi, yi, height]])

        n = np.append(normalFromSeg([x0, y0], [xi, yi]), 0)
        triangles.append(tri1)
        triangles.append(tri2)
    
        normals.append(n)
        normals.append(n)
        x0, y0, z0=[xi, yi, zi]
    return triangles, normals

def getWallsBuildings(buildings, height=-1):
    triangles=list()
    normals=list()
    i=0
    for b in buildings:
        t, n=getWalls(b[0], height)
        triangles.append(t)
        normals.append(n)
        i+=1
    return triangles, normals

def makeCircle(cx,cy,r,d=10):
    thetas = np.linspace(0, 2*np.pi, d)
    circle = [[cx+r * np.cos(theta), cy+r * np.sin(theta)] for theta in thetas]
    return circle

def getCityWallsAndTowersContour(roads,walls,wT,tR):
    wallSegs=getWallSegs(roads,walls,tR)
    walls=[]
    towers=[]
    i=0
    for seg in wallSegs:

        xr,yr=np.array(seg).transpose()#just lines
        cityWalls=contourFromLine(seg,wT) #contours of walls [[x1,y1],[x2,y2]...]
        walls.append(cityWalls)
        circles=[makeCircle(a,b,tR) for a,b in zip(xr,yr)]#contours of circles, makeCircle creates [[x1,x2,...],[y1,y2,...]]
        
        [towers.append(c) for c in circles]
       
    return walls,towers
        
def getWallSegs(roads,walls,towerRadius):
    wallseg=list()
    for w in walls:
        for what in w["coordinates"]:
            x,y=np.transpose(what)
            currentWallSeg=[]
            for i in range(len(x)):
                #plt.plot(x[i],y[i], "o", color="blue") #display point
                added=False
                for rc in roads: #iterate roads
                    roadWidth=rc["width"]
                    for xri,yri in rc['coordinates']:
                        if x[i]==xri and y[i]==yri:
                    #        plt.plot(xri,yri,"o",color="red")
                            #detected road. because we started at 1, we can always get x[i-1]
                            xp=x[-1] if i==0 else x[i-1]
                            yp=y[-1] if i==0 else y[i-1]

                            # we want a point that is at roadwidth/2+towerwidth/2 of the initial point, along the segment

                            leng=np.sqrt( (x[i]-xp)**2 + (y[i]-yp)**2 )
                            t=(leng-towerRadius/2-roadWidth/2)/leng
                            xnp1 = x[i]*t+xp*(1-t)
                            ynp1 = y[i]*t+yp*(1-t)
                     #       plt.plot(xnp1,ynp1,"o",color="yellow")

                            xn = x[0] if i==len(x)-1 else x[i+1]
                            yn = y[0] if i==len(x)-1 else y[i+1]
                            leng=np.sqrt( (x[i]-xn)**2 + (y[i]-yn)**2 )
                            
                            t=(leng-towerRadius-roadWidth/2-2)/leng#-2 for having a little offset from each side
                            xnp2 = x[i]*t+xn*(1-t)
                            ynp2 = y[i]*t+yn*(1-t)
                     #       plt.plot(xnp2,ynp2,"o",color="green")
                            currentWallSeg.append([xnp1,ynp1])
                            wallseg.append(currentWallSeg)
                            if i==len(x)-1:
                                wallseg[0].insert(0,[xnp2,ynp2])
                            else:
                                currentWallSeg=[[xnp2,ynp2]]
                            added=True


                if not added:
                    currentWallSeg.append([x[i],y[i]])
    return wallseg