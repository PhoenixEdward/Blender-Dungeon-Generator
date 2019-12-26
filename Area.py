try:
    from main import Vector2Int
except:
    pass

class Wall():
    def __init__(self):
        self.segments = []
        self.min = Vector2Int()
        self.max = Vector2Int()
        self.hasDoor = False

    def copy(self):
        return self

#change code so that it takes a list of tile values and produces this.

class Floor():
    def __init__(self, tiles):
        self.tiles = tiles

        x = []
        y = []

        for tile in tiles:
            x.append(tile[0])
            y.append(tile[1])

        self.xMax = max(x)
        self.xMin = min(x)
        self.yMax = max(y)
        self.yMin = min(y)
        self.width = self.xMax - self.xMin + 1
        self.height = self.yMax - self.yMin + 1

    def copy(self):
        return self

class Area():
    def __init__(self, tilemapper, floorTiles):
        self.roomIndex = tilemapper.roomIndex
        self.floor = Floor(floorTiles)
        self.walls = self.getWalls(tilemapper)

    def getWalls(self,tilemapper):
        walls = {
        "top": Wall(),
        "bottom": Wall(),
        "left": Wall(),
        "right": Wall()
        }

        tiles = self.floor
    ## wouldn't need to do this in c# with a public enum.
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
                        
        cornerTopLeft = Vector2Int(tiles.xMin - 1,tiles.yMax + 1)
        cornerBottomRight = Vector2Int(tiles.xMax + 1,tiles.yMin - 1)
            
        cornerBottomLeft = Vector2Int(tiles.xMin - 1,tiles.yMin - 1)
        cornerTopRight = Vector2Int(tiles.xMax - 1,tiles.yMax + 1)            

        walls["top"].min = cornerTopLeft
        walls["top"].max = cornerTopRight

        walls["bottom"].min = cornerBottomLeft
        walls["bottom"].max = cornerBottomRight

        walls["left"].min = cornerBottomLeft
        walls["left"].max = cornerTopLeft

        walls["right"].min = cornerBottomRight
        walls["right"].max = cornerTopRight
                

    ## layout "greedy" x walls

        ## add 3 due to the need to check current space as well as the 2 additional tiles added by wall depth.

        roomWidth = tiles.xMax - tiles.xMin + 3
            
        ##almost certainly need to add more to below. They will need to check incremented by 2 incase the first alternative is a corner

        ##check if tiles have been visited and adjust edges accordingingly
            
        startTop = walls["top"].min
        startBottom = walls["bottom"].min

        wallWidth = roomWidth

        push = 0

        while push < roomWidth:
            if startTop.x + push < tilemapper.map_width:
                if tilemapper.dmap[startTop.x + push,startTop.y] == TILE_WALL or tilemapper.dmap[startTop.x + push,startTop.y] == TILE_CORNER:
                    startTop = Vector2Int(startTop.x + push,startTop.y)
                    break
                elif tilemapper.dmap[startTop.x + push,startTop.y] == TILE_HALL:
                    walls["top"].hasDoor = True
                wallWidth -= 1
                push += 1
            else:
                startTop = Vector2Int(startTop.x + push - 1,startTop.y)
                break
            
                
        wallCount = 0
        lastCount = 0
                        
        for j in range(wallWidth):
            if startTop.x + j < tilemapper.map_width:
                if wallCount == lastCount:
                    if tilemapper.dmap[startTop.x + j, startTop.y] == TILE_WALL or tilemapper.dmap[startTop.x + j, startTop.y] == TILE_CORNER:
                        walls["top"].segments.append([Vector2Int(startTop.x+j,startTop.y)])
                        #tilemapper.dmap[startTop.x+j,startTop.y] = TILE_VISITED
                        wallCount += 1
                else:
                    if tilemapper.dmap[startTop.x + j, startTop.y] == TILE_WALL or tilemapper.dmap[startTop.x + j, startTop.y] == TILE_CORNER:
                        walls["top"].segments[lastCount].append(Vector2Int(startTop.x+j,startTop.y))
                        #tilemapper.dmap[startTop.x+j,startTop.y] = TILE_VISITED
                    elif tilemapper.dmap[startTop.x + j,startTop.y] == TILE_HALL:
                        walls["top"].hasDoor = True
                    else:
                        lastCount += 1
            
        wallWidth = roomWidth

        push = 0

        while push < roomWidth:
            if startBottom.x + push < tilemapper.map_width:
                if tilemapper.dmap[startBottom.x + push,startBottom.y] == TILE_WALL or tilemapper.dmap[startBottom.x + push,startBottom.y] == TILE_CORNER:
                    startBottom = Vector2Int(startBottom.x + push,startBottom.y)
                    break
                elif tilemapper.dmap[startBottom.x + push,startBottom.y] == TILE_HALL:
                    walls["bottom"].hasDoor = True
                wallWidth -= 1
                push += 1
            else:
                print("goof")
                startBottom = Vector2Int(startBottom.x + push -1,startBottom.y)
                break

        wallCount = 0
        lastCount = 0
                                    
        ## iterate for second x corner

        for j in range(wallWidth):
            if startBottom.x + j < tilemapper.map_width:
                if wallCount == lastCount:
                    if tilemapper.dmap[startBottom.x + j, startBottom.y] == TILE_WALL or tilemapper.dmap[startBottom.x + j, startBottom.y] == TILE_CORNER:
                        walls["bottom"].segments.append([Vector2Int(startBottom.x+j,startBottom.y)])
                        #tilemapper.dmap[startBottom.x+j,startBottom.y] = TILE_VISITED
                        wallCount += 1
                else:
                    if tilemapper.dmap[startBottom.x + j, startBottom.y] == TILE_WALL or tilemapper.dmap[startBottom.x + j, startBottom.y] == TILE_CORNER:
                        walls["bottom"].segments[lastCount].append(Vector2Int(startBottom.x+j,startBottom.y))
                        #tilemapper.dmap[startBottom.x+j,startBottom.y] = TILE_VISITED
                    elif tilemapper.dmap[startBottom.x + j,startBottom.y] == TILE_HALL:
                        walls["bottom"].hasDoor = True
                    else:
                        lastCount += 1

       

        roomHeight = tiles.yMax - tiles.yMin + 3

        startLeft = walls["left"].min
        startRight = walls["right"].min

        wallHeight = roomHeight

        push = 0

        ##possibly remove tile_corner

        while push < roomHeight:
            if startLeft.y + push < tilemapper.map_height:
                if tilemapper.dmap[startLeft.x,startLeft.y + push] == TILE_WALL or tilemapper.dmap[startLeft.x,startLeft.y+ push] == TILE_CORNER:
                    startLeft = Vector2Int(startLeft.x,startLeft.y+push)
                    break
                elif tilemapper.dmap[startLeft.x,startLeft.y+ push] == TILE_HALL:
                    walls["left"].hasDoor = True
                wallHeight -= 1
                push += 1
            else:
                print("Goof!")
                startLeft = Vector2Int(startLeft.x,startLeft.y+push - 1)
                break

        wallCount = 0
        lastCount = 0
            
        ## iterate for y corner
            
        for j in range(wallHeight):
            if startLeft.y + j < tilemapper.map_height:
                if wallCount == lastCount:
                    if tilemapper.dmap[startLeft.x, startLeft.y + j] == TILE_WALL:
                        walls["left"].segments.append([Vector2Int(startLeft.x,startLeft.y + j)])
                        #tilemapper.dmap[startLeft.x,startLeft.y + j] = TILE_VISITED
                        wallCount += 1
                else:
                    if tilemapper.dmap[startLeft.x, startLeft.y + j] == TILE_WALL:
                        walls["left"].segments[lastCount].append(Vector2Int(startLeft.x, startLeft.y+j))
                        #tilemapper.dmap[startLeft.x, startLeft.y+j] = TILE_VISITED
                    elif tilemapper.dmap[startLeft.x,startLeft.y + j] == TILE_HALL:
                        walls["left"].hasDoor = True
                    else:
                        lastCount += 1

        wallHeight = roomHeight

        push = 0

        while push < roomHeight:
            if startRight.y + push < tilemapper.map_height:
                if tilemapper.dmap[startRight.x,startRight.y+ push] == TILE_WALL or tilemapper.dmap[startRight.x,startRight.y+ push] == TILE_CORNER:
                    startRight = Vector2Int(startRight.x,startRight.y+ push)
                    break
                elif tilemapper.dmap[startRight.x,startRight.y+ push] == TILE_HALL:
                    walls["right"].hasDoor = True
                wallHeight -= 1
                push += 1
            else:
                break
        wallCount = 0
        lastCount = 0
            
        ##iterate for second y
            
        for j in range(wallHeight):
            if startRight.y + j < tilemapper.map_height:
                if wallCount == lastCount:
                    if tilemapper.dmap[startRight.x, startRight.y + j] == TILE_WALL:
                        walls["right"].segments.append([Vector2Int(startRight.x,startRight.y + j)])
                        #tilemapper.dmap[startRight.x,startRight.y + j] = TILE_VISITED
                        wallCount += 1
                else:
                    if tilemapper.dmap[startRight.x, startRight.y + j] == TILE_WALL:
                        walls["right"].segments[lastCount].append(Vector2Int(startRight.x,startRight.y + j))
                        #tilemapper.dmap[startRight.x, startRight.y+j] = TILE_VISITED
                    elif tilemapper.dmap[startRight.x,startRight.y + j] == TILE_HALL:
                        walls["right"].hasDoor = True
                    else:
                        lastCount += 1

        return walls

    def copy():
        return self


class Path(Area):
    def __init__(self, tilemapper, floorTiles, clearHorizontal):
        self.floor = Floor(floorTiles)
        self.walls = self.getWalls(tilemapper)
        self.clearHorizontal = clearHorizontal