[mcfg](https://watabou.itch.io/medieval-fantasy-city-generator) JSON to OBJ exporter 
====================
## export JSON to OBJ with customizable materials

Exemple file: Hiddenlight.json

result in [meshlab](http://www.meshlab.net/):
![Hiddenlight](https://github.com/Luvideria/mcfgJSONtoOBJ/raw/master/Hiddenlight.JPG)

## usage :
```bash
pip install tripy
python convert.py path/to/sourcefile.json path/to/objcreated
```
Do not put ".obj", it will be added automatically

Uses [tripy](https://github.com/linuxlewis/tripy) for triangulation of meshes.

### The up axis is the z axis !

Created OBJ file allows each object to be colored independantly

An object is:
- a road
- a field
- the earth
- walls of a building
- roof of a building

More specifically, each of these will have its own object and material:

```
o roof_245
usemtl roof_245
f 1234//567 ....
```

and in the mtl file the corresponding material:

```
newmtl earth_0
	 illum 4
	 Kd 0.26 0.53 0.19
	 Ks 0.2 0.5 0.2
	 Ka 0.4 0.4 0.4
	 Tf 1.0 1.0 1.0
	 Ns 20
	 Ni 1.0
```

As of today, the importer is not tested for city walls or river.

To create your own color scheme, change the functions in myColors.py:

```python
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
You can even create your own colors, it does not need to be fixed, use `random.random()` to create a number between 0 and 1. Add `import random` at the top of the file though.

Textures are not yet supported.
