## MCFG exporter https://watabou.itch.io/medieval-fantasy-city-generator
## export JSON to OBJ with materials

usage :
pip install tripy


the OBJ file created allows each object to be colored independantly
an object is:
- a road
- a field
- the earth
- walls of buildings
- roof of buildings

As of today, the importer is not tested for city walls or river.

To create your own color scheme, change the functions in myColors.py:

```
def getWallbColor():
	'''
	city walls color
	'''
    i=4
    kd=[0.46,0.03,0.09]
    ks=[0.3,0.01,0.02]
    ka=[0.2,0.01,0.01]
    tf=[1.0,1.0,1.0]
    ns=30
    ni=1.0
    return i,kd,ks,ka,tf,ns,ni
```
You can even create randomized colors within a palette. This is not yet implemented though.

Textures are not yet supported. (easy fix)
