

###THIS IS THE ONE I'M WORKING ON
from Area import *


try:
    import bpy
    import bmesh
    def print(data):
        for window in bpy.context.window_manager.windows:
            screen = window.screen
            for area in screen.areas:
                if area.type == 'CONSOLE':
                    override = {'window': window, 'screen': screen, 'area': area}
                    bpy.ops.console.scrollback_append(override, text=str(data), type="OUTPUT")
except:
    pass
    
from random import randint, choice, random, uniform, getrandbits
import numpy as np



# based on: https://gist.github.com/munificent/b1bcd969063da3e6c298be070a22b604 Robert Nystrom @munificentbob for Ginny 2008-2019
# and also from https://gist.github.com/Joker-vD/cc5372a349559b9d1a3b220d5eaf2b01

TILE_VOID        = 0 #' '
TILE_FLOOR       = 1 #'.'
TILE_WALL        = 2 #'#'
TILE_CORNER      = 3 #'!'
TILE_HALL        = 4 #'+'
TILE_PLAYER      = 6 #'@'
TILE_ROOM_CORNER = 7 #'?'
TILE_VISITED     = 8 #'$'
TILE_POPULAR     = 9 #'&'
TILE_WALL_CORNER = 10#'%'

class Vector2Int():
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

    def copy(self):
        return Vector2Int(self.x,self.y)

class Tile():
    def __init__(self, position, tileType):
        position = position

##probably turn self.tiles in to a floor object. Maybe same for walls just for consitency (maybe just inherit from RoomDims? Could change RoomDims into just room and it could store all the tile data as well. 
#Could just call the functions below to populate them... But it's part of a different class? and I can't do subclasses in python? Might have to wait for c#.

#-----------------------------------------------------------------------------------------------
class TileMapper(object):
    """build a map of interconnected rooms"""
    def __init__(self, width=80, height=40, roomCount=5):
        self.map_width=width
        self.map_height=height
        self.dmap=np.zeros((width, height), dtype=np.uint8)
        self.roomIndex = 0
        self.roomCount = roomCount
        self.rmap=np.zeros((width, height), dtype=np.uint8)
        self.areas = []

    #-----------------------------------------------------------------------------------------------
    def generate(self):
        for i in range(1000):
            check = self.cave(i==0)
            if check == True:
                self.roomIndex += 1
            if self.roomIndex == self.roomCount:
                break

    #-----------------------------------------------------------------------------------------------
    def cave(self, first_room):
        width=randint(10,15)
        height=randint(10,15)
        x0=randint(2,self.map_width - width - 1) - 2
        y0=randint(2,self.map_height - height -1) - 2
        x1=x0 + width + 2
        y1=y0 + height + 2
        floorTiles = []

        for y in range(y0, y1):
            for x in range(x0, x1):
                if self.dmap[x,y]==TILE_FLOOR:      #if the new room toches any other floor OR hallway then this room is invalid
                    return False

        doors=[]    #list of potential doors
        if not first_room:
            for y in range(y0, y1):
                for x in range(x0, x1):
                    s=(x==x0 or x==x1-1)
                    t=(y==y0 or y==y1-1)
                    if not (s and t):           #dont make a door on a corner
                        if (s or t) and (self.dmap[x,y]==TILE_WALL):  #only make a door on the perimeter and where it intesects another wall
                            doors.append((x,y))     #build list of potential doors
            halls = []

            for door in doors:

                clearTop = False
                clearBottom = False
                clearLeft = False
                clearRight = False

                j=0

                for i in range(door[0],x1+1):
                    #print("check: " + str(i) + " Door x:" + str(door[0]), " Max X: " + str(x1))
                    if self.dmap[i, door[1]] != TILE_WALL or self.dmap[ i, door[1]] == TILE_CORNER:
                        break
                    else:
                        j+=1
                    if j >= 2:
                        clearRight = True
                j=0
                for i in range(door[0],x0-1,-1):
                    if self.dmap[i, door[1]] != TILE_WALL or self.dmap[ i, door[1]] == TILE_CORNER:
                        break
                    else:
                        j+=1
                    if j >= 2:
                        clearLeft = True
                j=0
                for i in range(door[1],y1+1):
                    if self.dmap[door[0], i] != TILE_WALL or self.dmap[door[0], i] == TILE_CORNER:
                        break
                    else:
                        j+=1
                        #print(j)
                    if j >= 2:
                        clearTop = True
                j=0
                for i in range(door[1],y0-1,-1):
                    if self.dmap[door[0], i] != TILE_WALL or self.dmap[door[0], i] == TILE_CORNER:
                        break
                    else:
                        j+=1
                    if j >= 2:
                        clearBottom = True
                
                clearHorizontal = None
                hallTiles = []

                if clearLeft and clearRight:
                    clearHorizontal = True
                    if door[1] == y0:
                        rando = bool(getrandbits(1))
                        rando2 = bool(getrandbits(1))
                        if rando == 0:
                            hallTiles.append(door)
                            hallTiles.append([door[0], door[1]-1])
                            if rando2 == 1:
                                hallTiles.append([door[0]-1,door[1]])
                                hallTiles.append([door[0]-1, door[1]-1])
                                hallTiles.append([door[0]-2,door[1]])
                                hallTiles.append([door[0]-2, door[1]-1])

                        if rando == 1:
                            hallTiles.append(door)
                            hallTiles.append([door[0], door[1]-1])
                            if rando2 == 1:
                                hallTiles.append([door[0]+1,door[1]])
                                hallTiles.append([door[0]+1, door[1]-1])
                                hallTiles.append([door[0]+2,door[1]])
                                hallTiles.append([door[0]+2, door[1]-1])

                    if door[1] == y1:
                        rando = bool(getrandbits(1))
                        rando2 = bool(getrandbits(1))
                        if rando == 0:
                            hallTiles.append(door)
                            hallTiles.append([door[0], door[1]+1])
                            if rando2 == 0:
                                hallTiles.append([door[0]-1, door[1]+1])
                                hallTiles.append([door[0]-1,door[1]])
                                hallTiles.append([door[0]-2, door[1]+1])
                                hallTiles.append([door[0]-2,door[1]])
                        if rando == 1:
                            hallTiles.append(door)
                            hallTiles.append([door[0], door[1]+1])
                            if rando2 == 0:
                                hallTiles.append([door[0]+1,door[1]])
                                hallTiles.append([door[0]+1, door[1]+1])
                                hallTiles.append([door[0]+2,door[1]])
                                hallTiles.append([door[0]+2, door[1]+1])

                if clearTop and clearBottom:
                    clearHorizontal = False
                    if door[0] == x0:
                        rando = bool(getrandbits(1))
                        rando2 = bool(getrandbits(1))
                        if rando == 0:
                            hallTiles.append(door)
                            hallTiles.append([door[0]-1, door[1]])
                            if rando2 == 1:
                                hallTiles.append([door[0],door[1]-1])
                                hallTiles.append([door[0]-1, door[1]-1])
                                hallTiles.append([door[0], door[1]-2])
                                hallTiles.append([door[0]-1, door[1]-2])

                        if rando == 1:
                            hallTiles.append(door)
                            hallTiles.append([door[0]-1, door[1]])
                            if rando2 == 1:
                                hallTiles.append([door[0],door[1]+1])
                                hallTiles.append([door[0]-1, door[1]+1])
                                hallTiles.append([door[0],door[1]+2])
                                hallTiles.append([door[0]-1, door[1]+2])
                    if door[1] == x1:
                        rando = bool(getrandbits(1))
                        rando2 = bool(getrandbits(1))
                        if rando == 0:
                            hallTiles.append(door)
                            hallTiles.append([door[0]+1, door[1]])
                            if rando2 == 1:
                                hallTiles.append([door[0]+2,door[1]-1])
                                hallTiles.append([door[0]+1, door[1]-1])
                                hallTiles.append([door[0]+1,door[1]])
                                hallTiles.append([door[0]+2,door[1]])
                        if rando == 1:
                            hallTiles.append(door)
                            hallTiles.append([door[0],door[1]+1])
                            if rando2 == 1:
                                hallTiles.append([door[0]+1, door[1]+1])
                                hallTiles.append([door[0]+1, door[1]])
                                hallTiles.append([door[0]+2, door[1]+1])
                                hallTiles.append([door[0]+2, door[1]])
                                
                if len(hallTiles) > 0:
                    halls.append(Path(self, hallTiles, clearHorizontal))

            if len(halls)==0:
                return False
        
        if not first_room:
            door=choice(halls)
            for tile in door.floor.tiles:
                self.dmap[tile[0], tile[1]]=TILE_HALL 
            if door.floor.xMax == x0 and door.clearHorizontal == False:
                x0 = x0 + door.floor.width
            elif door.floor.xMin == x1 and door.clearHorizontal == False:
                x1 = x1 - door.floor.width
            if door.floor.yMax == y0 and door.clearHorizontal == True:
                y0 = y0 + door.floor.height
            elif door.floor.yMin == x1 and door.clearHorizontal == True:
                y1 = y1 - door.floor.height

        floorTiles = []
                #if we got this far we have a valid room so carve it out of the void
        for y in range(y0, y1):
            for x in range(x0, x1): 
                if self.dmap[x,y]!=TILE_CORNER:     #dont over write another corner
                    s=(x==x0 or x==x1-1)
                    t=(y==y0 or y==y1-1)
                    if s and t:
                        self.dmap[x,y]=TILE_CORNER
                    elif s or t:
                        self.dmap[x,y]=TILE_WALL
                    else:
                        self.dmap[x,y]=TILE_FLOOR
                        self.rmap[x,y]=self.roomIndex
                        floorTiles.append([x,y])

        area = Area(self,floorTiles)

        if first_room:
            h=randint(0,width-1)+x0+1
            v=randint(0,height-1)+y0+1
            self.dmap[h,v]=TILE_PLAYER
        
        self.areas.append(area)

        return True
            #add any other items or npcs to the rooms here. see player random location for example

    #-----------------------------------------------------------------------------------------------
    def print_map(self):
        #change the TILE_CORNER to another character such as ! to see the corners in the map.        
        for k in range(len(self.areas)):
            v = self.areas[k].floor
            self.dmap[v.xMax,v.yMax] = TILE_ROOM_CORNER
            self.dmap[v.xMin,v.yMax] = TILE_ROOM_CORNER
            self.dmap[v.xMax,v.yMin] = TILE_ROOM_CORNER
            self.dmap[v.xMin,v.yMin] = TILE_ROOM_CORNER
            
                #change the TILE_CORNER to another character such as ! to see the corners in the map.
        icons={TILE_VOID:' ', TILE_FLOOR:'.', TILE_WALL:'#', TILE_CORNER:'!', TILE_HALL:'+', TILE_PLAYER:'@', TILE_ROOM_CORNER:'?', TILE_VISITED:'$',TILE_POPULAR:'&', TILE_WALL_CORNER:'%'}
        for v in range(self.map_height-1, -1,-1):
            ln=''
            for h in range(self.map_width):
                if self.dmap[h,v] == TILE_FLOOR:
                    ln+=str(self.rmap[h,v])
                else:
                    ln+=icons[self.dmap[h,v]]
            print(ln)

    #-----------------------------------------------------------------------------------------------

    def getLevelData(self):
        return self.areas

   
    def render(self):
        
        bpyscene = bpy.context.scene
        
        for room in range(len(self.areas)):
            
            v = self.areas[room].floor
            
            mesh = bpy.data.meshes.new('room' + str(room))
            basic_cube = bpy.data.objects.new('room' + str(room), mesh)

            # Add the object into the scene.
            bpyscene.collection.objects.link(basic_cube)
            igloo = bpy.context.window.scene.objects['room' + str(room)]
            bpy.context.view_layer.objects.active = igloo
            basic_cube.select_set(True)

            # Construct the bmesh cube and assign it to the blender mesh.
            bm = bmesh.new()
            bmesh.ops.create_cube(bm, size=1.0)
            bm.to_mesh(mesh)
            bm.free()

            bpy.ops.transform.resize(value=(v.width, v.height, 1))

            bpy.ops.transform.translate(value=(v.xMax-(v.width/2), v.yMax-(v.height/2), 0.5))

            activeObject = bpy.context.active_object #Set active object to variable
            
            mat = bpy.data.materials["floor" + str(room)]
            
            activeObject.data.materials.append(mat)
            
            basic_cube.select_set(False)
            
            
        ## generate walls
        
            for side in self.areas[room].walls.keys():
            
                wall = self.areas[room].walls[side]
                
                s = 0        
                    
                if side == "top" or side == "bottom":
                    
                    for seg in self.areas[room].walls[side].segments:
                        
                        mesh = bpy.data.meshes.new('wall' + str(room) + side + str(s))
                        basic_cube = bpy.data.objects.new('wall' + str(room) + side + str(s), mesh)

                        # Add the object into the scene.
                        bpyscene.collection.objects.link(basic_cube)
                        igloo = bpy.context.window.scene.objects['wall' + str(room) + side + str(s)]
                        bpy.context.view_layer.objects.active = igloo
                        basic_cube.select_set(True)

                        # Construct the bmesh cube and assign it to the blender mesh.
                        bm = bmesh.new()
                        bmesh.ops.create_cube(bm, size=1.0)
                        bm.to_mesh(mesh)
                        bm.free()
                    
                        length = seg[-1].x - seg[0].x + 1
                        
            
                        bpy.ops.transform.resize(value=(length, 1, 2))
                        
                        bpy.ops.transform.translate(value=(seg[-1].x-(length/2), seg[0].y-0.5, 0.5))
                        
                        activeObject = bpy.context.active_object #Set active object to variable
                
                        mat = bpy.data.materials["Rando" + str(room)]
                
                        activeObject.data.materials.append(mat)
                
                        basic_cube.select_set(False)
                        
                        s += 1        
                    
                elif side == "left" or side == "right":
                    
                    for seg in self.areas[room].walls[side].segments:
                        
                        
                        mesh = bpy.data.meshes.new('wall' + str(room) + side + str(s))
                        basic_cube = bpy.data.objects.new('wall' + str(room) + side + str(s), mesh)

                        # Add the object into the scene.
                        bpyscene.collection.objects.link(basic_cube)
                        igloo = bpy.context.window.scene.objects['wall' + str(room) + side + str(s)]
                        bpy.context.view_layer.objects.active = igloo
                        basic_cube.select_set(True)

                        # Construct the bmesh cube and assign it to the blender mesh.
                        bm = bmesh.new()
                        bmesh.ops.create_cube(bm, size=1.0)
                        bm.to_mesh(mesh)
                        bm.free()
                                        
                        length = seg[-1].y - seg[0].y + 1
                                    
                        bpy.ops.transform.resize(value=(1, length, 2))
                        
                        bpy.ops.transform.translate(value=(seg[-1].x-0.5,seg[-1].y-(length/2), 0.5))
                        
                        activeObject = bpy.context.active_object #Set active object to variable
                
                        mat = bpy.data.materials["Rando" + str(room)]
                
                        activeObject.data.materials.append(mat)
                
                        basic_cube.select_set(False)
                        
                        s+=1 
            
 
        ## generate doors
        
        k = 0
            
            
        for v in range(self.map_height):
            for h in range(self.map_width):
                if self.dmap[h,v] == TILE_HALL or self.dmap[h,v] == TILE_HALL:
                    
                    mesh = bpy.data.meshes.new('door' + str(k))
                    basic_cube = bpy.data.objects.new('door' + str(k), mesh)

                    # Add the object into the scene.
                    bpyscene.collection.objects.link(basic_cube)
                    igloo = bpy.context.window.scene.objects['door' + str(k)]
                    bpy.context.view_layer.objects.active = igloo
                    basic_cube.select_set(True)

                    # Construct the bmesh cube and assign it to the blender mesh.
                    bm = bmesh.new()
                    bmesh.ops.create_cube(bm, size=1.0)
                    bm.to_mesh(mesh)
                    bm.free()

                    bpy.ops.transform.resize(value=(1, 1, 1))

                    bpy.ops.transform.translate(value=(h-.5, v-.5, 0.5))

                    activeObject = bpy.context.active_object #Set active object to variable

                    mat = bpy.data.materials["Door"]
                    
                    activeObject.data.materials.append(mat)

                    
                    basic_cube.select_set(False)
                    
                    k += 1

#-----------------------------------------------------------------------------------------------

if __name__ == '__main__':
    cr=TileMapper(50,50,6)
    cr.generate()
    cr.print_map()
    #cr.render()