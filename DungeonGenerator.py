

###THIS IS THE ONE I'M WORKING ON


'''
import bpy
import bmesh
def print(data):
    for window in bpy.context.window_manager.windows:
        screen = window.screen
        for area in screen.areas:
            if area.type == 'CONSOLE':
                override = {'window': window, 'screen': screen, 'area': area}
                bpy.ops.console.scrollback_append(override, text=str(data), type="OUTPUT")
'''

import sys
if sys.version_info[0] < 3: 
    from StringIO import StringIO
else:
    from io import StringIO

import pandas as pd

    
from random import randint, choice, random, uniform
import numpy as np



# based on: https://gist.github.com/munificent/b1bcd969063da3e6c298be070a22b604 Robert Nystrom @munificentbob for Ginny 2008-2019
# and also from https://gist.github.com/Joker-vD/cc5372a349559b9d1a3b220d5eaf2b01

TILE_VOID        = 0 #' '
TILE_FLOOR       = 1 #'.'
TILE_WALL        = 2 #'#'
TILE_CORNER      = 3 #'!'
TILE_OPEN_DOOR   = 4 #'+'
TILE_CLOSED_DOOR = 5 #'*'
TILE_PLAYER      = 6 #'@'
TILE_ROOM_CORNER = 7 #'?'
TILE_VISITED     = 8 #'$'
TILE_POPULAR     = 9 #'&'
TILE_WALL_CORNER = 10#'%'
#-----------------------------------------------------------------------------------------------
class ConnectedRooms(object):
    """build a map of interconnected rooms"""
    def __init__(self, width=80, height=40, roomCount=5):
        self.map_width=width
        self.map_height=height
        self.dmap=np.zeros((width, height), dtype=np.uint8)
        self.roomIndex = 0
        self.roomCount = roomCount
        self.rmap=np.zeros((width, height), dtype=np.uint8)
        self.proof=np.zeros((width, height), dtype=np.uint8) 
        self.roomTiles = [None] * roomCount
        self.roomDims = {}
        self.wallTilesX = {}
        self.wallTilesY =  {}
        #may not need
        self.wallDims = {}

    #-----------------------------------------------------------------------------------------------
    def generate(self):
        for i in range(1000):
            check = self.cave(i==0)
            if check == True:
                self.roomIndex += 1
            if self.roomIndex == self.roomCount:
                break
        self.proof = self.dmap.copy()

    #-----------------------------------------------------------------------------------------------
    def cave(self, first_room):
        width=randint(5,15)
        height=randint(5,15)
        x0=randint(2,self.map_width - width - 1) - 2
        y0=randint(2,self.map_height - height -1) - 2
        x1=x0 + width + 2
        y1=y0 + height + 2

        for y in range(y0, y1):
            for x in range(x0, x1):
                if self.dmap[x,y]==TILE_FLOOR:      #if the new room toches any other floor then this room is invalid
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
            if len(doors)==0:   #if we didnt find any doors then this is not valid room attached to another room
                return False

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

        if first_room:
            h=randint(0,width-1)+x0+1
            v=randint(0,height-1)+y0+1
            self.dmap[h,v]=TILE_PLAYER
        else:
            door=choice(doors)
            dtype=choice([TILE_OPEN_DOOR, TILE_CLOSED_DOOR, TILE_OPEN_DOOR])
            self.dmap[door[0], door[1]]=dtype
        
        return True
            #add any other items or npcs to the rooms here. see player random location for example

    #-----------------------------------------------------------------------------------------------
    def print_map(self):
        #change the TILE_CORNER to another character such as ! to see the corners in the map.        
        for k in self.roomDims.keys():
            v = self.roomDims[k]["floor"]
            self.proof[v["xMax"],v["yMax"]] = TILE_ROOM_CORNER
            self.proof[v["xMin"],v["yMax"]] = TILE_ROOM_CORNER
            self.proof[v["xMax"],v["yMin"]] = TILE_ROOM_CORNER
            self.proof[v["xMin"],v["yMin"]] = TILE_ROOM_CORNER
            
                #change the TILE_CORNER to another character such as ! to see the corners in the map.
        icons={TILE_VOID:' ', TILE_FLOOR:'.', TILE_WALL:'#', TILE_CORNER:'!', TILE_OPEN_DOOR:'+', TILE_CLOSED_DOOR:'*', TILE_PLAYER:'@', TILE_ROOM_CORNER:'?', TILE_VISITED:'$',TILE_POPULAR:'&', TILE_WALL_CORNER:'%'}
        for v in range(self.map_height):
            ln=''
            for h in range(self.map_width):
                if self.proof[h,v] == TILE_FLOOR:
                    ln+=str(self.rmap[h,v])
                else:
                    ln+=icons[self.proof[h,v]]
            print(ln)
    
            
    #-----------------------------------------------------------------------------------------------
    def print_df(self):
                
        df_string = ""
        
        for i in range(self.map_width):
            if i < self.map_width - 1:
                df_string += str(i) + ";"
            else:
                df_string += str(i) + "\n"
        
        for k in self.roomDims.keys():
            v = self.roomDims[k]["floor"]
            self.proof[v["xMax"],v["yMax"]] = TILE_ROOM_CORNER
            self.proof[v["xMin"],v["yMax"]] = TILE_ROOM_CORNER
            self.proof[v["xMax"],v["yMin"]] = TILE_ROOM_CORNER
            self.proof[v["xMin"],v["yMin"]] = TILE_ROOM_CORNER
            
                #change the TILE_CORNER to another character such as ! to see the corners in the map.
        icons={TILE_VOID:' ', TILE_FLOOR:'.', TILE_WALL:'#', TILE_CORNER:'!', TILE_OPEN_DOOR:'+', TILE_CLOSED_DOOR:'*', TILE_PLAYER:'@', TILE_ROOM_CORNER:'?', TILE_VISITED:'$',TILE_POPULAR:'&', TILE_WALL_CORNER:'%'}
        for v in range(self.map_height):
            ln=''
            for h in range(self.map_width):
                if self.proof[h,v] == TILE_FLOOR:
                    ln+=str(self.rmap[h,v])+";"
                else:
                    ln+=icons[self.proof[h,v]]+";"
            df_string += ln + "\n"
            
        return df_string
            
    #-----------------------------------------------------------------------------------------------
    def getFloorDims(self):
        for v in range(self.map_height):
            for h in range(self.map_width):
                if self.dmap[h,v] == TILE_FLOOR:
                    roomKey = self.rmap[h,v]
                    if self.roomTiles[roomKey] == None:
                        self.roomTiles[roomKey] = [[],[]]
                        self.roomTiles[roomKey][0].append(h)
                        self.roomTiles[roomKey][1].append(v)
                    else:
                        self.roomTiles[roomKey][0].append(h)
                        self.roomTiles[roomKey][1].append(v)
                    
        for i in range(self.roomCount):
            self.roomDims[i] = {}
            self.roomDims[i]["floor"] = {
                "xMax": max(self.roomTiles[i][0]),
                "xMin": min(self.roomTiles[i][0]),
                "yMax": max(self.roomTiles[i][1]),
                "yMin": min(self.roomTiles[i][1]),
                "width": max(self.roomTiles[i][0]) - min(self.roomTiles[i][0]) + 1,
                "height": max(self.roomTiles[i][1]) - min(self.roomTiles[i][1]) + 1,
            }
            
            
    def getWallDims(self):
                
        # change corner names to represent waht the actual god damn corners they represent are.

        for room in self.roomDims.keys():

            tiles = self.roomDims[room]["floor"]

            roomWidth = tiles["xMax"] - tiles["xMin"] + 2
            roomHeight = tiles["yMax"] - tiles["yMin"] + 2
                        
            corner_x = [tiles["xMin"] - 1,tiles["yMax"] + 1]
            corner_y = [tiles["xMax"] + 1,tiles["yMin"] - 1]
            
            corner_z = [tiles["xMin"] - 1,tiles["yMin"] - 1]
            corner_w = [tiles["xMin"] - 1,tiles["yMin"] - 1]

            ## grab unused corner for data purposes. Right wall Bottom
            ## potentiall rename to just Max and Min. 

            corner_u = [tiles["xMax"] - 1,tiles["yMax"] + 1]

            self.roomDims[room]["walls"] = {}

            walls = self.roomDims[room]["walls"]

            walls["top"] = {
                "min": corner_x,
                "max": corner_u
                }

            walls["bottom"] = {
                "min": corner_z,
                "max": corner_y
                }

            walls["left"] = {
                "min": corner_x,
                "max": corner_z
                }

            walls["right"] = {
                "min": corner_y,
                "max": corner_u,
                }
            
            ##almost certainly need to add more to below. They will need to check incremented by 2 incase the first alternative is a corner

            ##check if tiles have been visited and adjust edges accordingingly

            if self.proof[corner_x[0],corner_x[1]] == TILE_WALL or self.proof[corner_x[0],corner_x[1]] == TILE_CORNER:
                pass
            elif self.proof[corner_x[0] + 1,corner_x[1]] == TILE_WALL or self.proof[corner_x[0] + 1,corner_x[1]] == TILE_CORNER:
                corner_x = [corner_x[0] + 1,corner_x[1]]
                
            ## do the same for y this time allowing for corners
            if self.proof[corner_y[0],corner_y[1]] == TILE_WALL or self.proof[corner_y[0],corner_y[1]] == TILE_CORNER:
                pass
            elif self.proof[corner_y[0],corner_y[1]-1] == TILE_WALL or self.proof[corner_y[0],corner_y[1]-1] == TILE_CORNER:
                corner_y = [corner_y[0],corner_y[1]-1]
            
            
            ## below corners are technically the same but fall back on seperate cells if initial is blocked. Also y allows for corners
            if self.proof[corner_z[0],corner_z[1]] == TILE_WALL or self.proof[corner_z[0],corner_z[1]] == TILE_CORNER:
                pass
            elif self.proof[corner_z[0]+1,corner_z[1]] == TILE_WALL or self.proof[corner_z[0]+1,corner_z[1]] == TILE_CORNER:
                corner_z = [corner_z[0]+1,corner_z[1]]
                            
            if self.proof[corner_w[0],corner_w[1]] == TILE_WALL or self.proof[corner_w[0],corner_w[1]] == TILE_CORNER:
                pass
            elif self.proof[corner_w[0],corner_w[1]-1] == TILE_WALL or self.proof[corner_w[0],corner_w[1]-1] == TILE_CORNER:
                corner_w = [corner_w[0],corner_w[1]-1]
            
            
                
            wallCount = 0
            lastCount = 0
            
            walls["top"]["segments"] = []
            
            for j in range(roomWidth):
                if corner_x[0] + j < self.map_width:
                    if wallCount == lastCount:
                        if self.proof[corner_x[0] + j, corner_x[1]] == TILE_WALL or self.proof[corner_x[0] + j, corner_x[1]] == TILE_CORNER:
                            walls["top"]["segments"].append([[corner_x[0]+j,corner_x[1]]])
                            self.proof[corner_x[0]+j,corner_x[1]] = TILE_VISITED
                            wallCount += 1
                    else:
                        if self.proof[corner_x[0] + j, corner_x[1]] == TILE_WALL or self.proof[corner_x[0] + j, corner_x[1]] == TILE_CORNER:
                            walls["top"]["segments"][lastCount].append([corner_x[0]+j,corner_x[1]])
                            self.proof[corner_x[0]+j,corner_x[1]] = TILE_VISITED
                        else:
                            lastCount += 1

            wallCount = 0
            lastCount = 0
            
            walls["bottom"]["segments"] = []
                        
            ## iterate for second x corner

            for j in range(roomWidth):
                if corner_z[0] + j < self.map_width:
                    if wallCount == lastCount:
                        if self.proof[corner_z[0] + j, corner_z[1]] == TILE_WALL or self.proof[corner_x[0] + j, corner_x[1]] == TILE_CORNER:
                            walls["bottom"]["segments"].append([[corner_z[0]+j,corner_z[1]]])
                            self.proof[corner_z[0]+j,corner_z[1]] = TILE_VISITED
                            wallCount += 1
                    else:
                        if self.proof[corner_z[0] + j, corner_z[1]] == TILE_WALL or self.proof[corner_x[0] + j, corner_x[1]] == TILE_CORNER:
                            walls["bottom"]["segments"][lastCount].append([corner_z[0]+j,corner_z[1]])
                            self.proof[corner_z[0]+j,corner_z[1]] = TILE_VISITED
                        else:
                            lastCount += 1
            
            wallCount = 0
            lastCount = 0      
            
            walls["left"]["segments"] = []

            ## iterate for y corner in reverse
            
            for j in range(roomHeight,-1,-1):
                if wallCount == lastCount:
                    if self.proof[corner_w[0], corner_w[1] + j] == TILE_WALL or self.proof[corner_w[0], corner_w[1] + j] == TILE_CORNER:
                        walls["left"]["segments"].append([[corner_w[0],corner_w[1] + j]])
                        self.proof[corner_w[0],corner_w[1] + j] = TILE_VISITED
                        wallCount += 1
                else:
                    if self.proof[corner_w[0], corner_w[1]+j] == TILE_WALL or self.proof[corner_w[0], corner_w[1]+j] == TILE_CORNER:
                        walls["left"]["segments"][lastCount].append([corner_w[0], corner_w[1]+j])
                        self.proof[corner_w[0], corner_w[1]+j] = TILE_VISITED
                    else:
                        lastCount += 1

            wallCount = 0
            lastCount = 0
            
            walls["right"]["segments"] = []

            ##iterate for second y in reverse
            
            for j in range(roomHeight,-1,-1):
                if wallCount == lastCount:
                    if self.proof[corner_y[0], corner_y[1] + j] == TILE_WALL or self.proof[corner_y[0], corner_y[1] + j] == TILE_CORNER:
                        walls["right"]["segments"].append([[corner_y[0],corner_y[1] + j]])
                        self.proof[corner_y[0],corner_y[1] + j] = TILE_VISITED
                        wallCount += 1
                else:
                    if self.proof[corner_y[0], corner_y[1]+j] == TILE_WALL or self.proof[corner_y[0], corner_y[1]+j] == TILE_CORNER:
                        walls["right"]["segments"][lastCount].append([corner_y[0],corner_y[1] + j])
                        self.proof[corner_y[0], corner_y[1]+j] = TILE_VISITED
                    else:
                        lastCount += 1
                        
            wallCount = 0
            lastCount = 0           

                        
    def getLevelData(self):
        return self.roomDims

'''    
def render(self):
        
        bpyscene = bpy.context.scene
        
        for k,v in self.roomDims.items():
            
            mesh = bpy.data.meshes.new('New' + str(k))
            basic_cube = bpy.data.objects.new('New' + str(k), mesh)

            # Add the object into the scene.
            bpyscene.collection.objects.link(basic_cube)
            igloo = bpy.context.window.scene.objects['New' + str(k)]
            bpy.context.view_layer.objects.active = igloo
            basic_cube.select_set(True)

            # Construct the bmesh cube and assign it to the blender mesh.
            bm = bmesh.new()
            bmesh.ops.create_cube(bm, size=1.0)
            bm.to_mesh(mesh)
            bm.free()

            bpy.ops.transform.resize(value=(v["width"], v["height"], 1))

            bpy.ops.transform.translate(value=(v["xMax"]-(v["width"]/2), v["yMax"]-(v["height"]/2), 0.5))

            activeObject = bpy.context.active_object #Set active object to variable
            
            mat = bpy.data.materials["Rando" + str(k)]
            
            activeObject.data.materials.append(mat)
            
            basic_cube.select_set(False)
            
        
        k = self.roomCount + 1
            
        for v in range(self.map_height):
            for h in range(self.map_width):
                if self.dmap[h,v] == TILE_OPEN_DOOR or self.dmap[h,v] == TILE_CLOSED_DOOR:
                    
                    mesh = bpy.data.meshes.new('New' + str(k))
                    basic_cube = bpy.data.objects.new('New' + str(k), mesh)

                    # Add the object into the scene.
                    bpyscene.collection.objects.link(basic_cube)
                    igloo = bpy.context.window.scene.objects['New' + str(k)]
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
#TILE_WALL        
#TILE_CORNER      
#TILE_OPEN_DOOR   
#TILE_CLOSED_DOOR 
#TILE_PLAYER      
#TILE_ROOM_CORNER

'''
    
#-----------------------------------------------------------------------------------------------

if __name__ == '__main__':
    cr=ConnectedRooms(50,50,6)
    cr.generate()
    cr.getFloorDims()
    cr.getWallDims()
    cr.print_map()
    #cr.render()