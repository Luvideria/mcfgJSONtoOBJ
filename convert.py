import json
import numpy as np
import sys
import os
import tripy

#get arguments
from to3D import *
from toOBJ import *

if not len(sys.argv)==3:
	print("Usage: python convert.py file.json outputname")
	print("outputname will be created as outputname.obj")
	exit()
loc=sys.argv[1]
fn=sys.argv[2]


file=open(loc, "r")
data=json.loads(file.read())

towerRadius=data["features"][0]["towerRadius"]
wallThickness=data["features"][0]["wallThickness"]

earth=data["features"][1]["coordinates"]
roads=data["features"][2]["geometries"]
walls=data["features"][3]["geometries"]
buildings=data["features"][6]["coordinates"]
fields=data["features"][10]["coordinates"]
square=data["features"][8]["coordinates"]
prisms=data["features"][7]["coordinates"]


wallsContour,towersContour=getCityWallsAndTowersContour(roads,walls,wallThickness,towerRadius)

#you can specify the width here, common for all roads though. modify getRoads for another behavior
earthtri, earthn = getEarth(earth[0])
roadtri, roadn = getRoads(roads)
fieldtri, fieldn = getFields(fields, 0.1)#at 0.1, it creates a flat surface, above, it creates a bloc similar to a building, but walls and roof are not separated
rooftri, roofn = getSurfaces(buildings, 8)
wallbtri, wallbn = getWallsBuildings(buildings, 8)
citywalltri,citywalln=getCityWalls(wallsContour,10)
citytowertri,citytowern=getCityWalls(towersContour,12)
squaretri, squaren = getSurfaces(square, 0.1)
prismstri, prismsn = getSurfaces(prisms, 0.1)


file=open(fn+".obj", "w")
file.write("mtllib "+fn+".mtl\n")

writeTriangleArray(earthtri, file)
for road in roadtri:
    writeTriangleArray(road, file)
for field in fieldtri:
    writeTriangleArray(field, file)
for roof in rooftri:
    writeTriangleArray(roof, file)
for wallb in wallbtri:
    writeTriangleArray(wallb, file)
for cityw in citywalltri:
    writeTriangleArray(cityw, file)
for cityt in citytowertri:
    writeTriangleArray(cityt, file)
for s in squaretri:
    writeTriangleArray(s, file)
for p in prismstri:
    writeTriangleArray(p, file)

writeNormalArray(earthn, file)
for road in roadn:
    writeNormalArray(road, file)
for field in fieldn:
    writeNormalArray(field, file)
for roof in roofn:
    writeNormalArray(roof, file)
for wallb in wallbn:
    writeNormalArray(wallb, file)
for cityw in citywalln:
    writeNormalArray(cityw, file)
for cityt in citytowern:
    writeNormalArray(cityt, file)
for s in squaren:
    writeNormalArray(s, file)
for p in prismsn:
    writeNormalArray(p, file)

counter=1
counter=writeObjects([earthn], file, counter, "earth")
counter=writeObjects(roadn, file, counter, "road")
counter=writeObjects(fieldn, file, counter, "field")
counter=writeObjects(roofn, file, counter, "roof")
counter=writeObjects(wallbn, file, counter, "wallb")
counter=writeObjects(citywalln, file, counter, "citywall")
counter=writeObjects(citytowern, file, counter, "citytower")
counter=writeObjects(squaren, file, counter, "square")
counter=writeObjects(prismsn, file, counter, "prisms")


mtl=open(fn+".mtl", "w")

writeMTL([earthn], mtl, "earth")
writeMTL(roadn, mtl, "road")
writeMTL(fieldn, mtl, "field")
writeMTL(roofn, mtl, "roof")
writeMTL(wallbn, mtl, "wallb")
writeMTL(citywalln, mtl, "citywall")
writeMTL(citytowern, mtl, "citytower")
writeMTL(squaren, mtl, "square")
writeMTL(prismsn, mtl, "prisms")