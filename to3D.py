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

def getField(field, height=0.1):
    '''
    field: a contour [[x, y], [x, y]]
    returns either a plane that has height just above the ground (0) or a surface with walls
    '''
    doWalls=False
    triangles=list()
    normals=list()
    field.append(field[0]) #to got a closed loop
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