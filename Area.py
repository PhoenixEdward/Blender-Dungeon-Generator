from main import Vector2Int

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
        self.xMax = max(tiles[0])
        self.xMin = min(tiles[0])
        self.yMax = max(tiles[1])
        self.yMin = min(tiles[1])
        self.width = max(tiles[0]) - min(tiles[0]) + 1
        self.height = max(tiles[1]) - min(tiles[1]) + 1

    def copy(self):
        return self

class Area():
    def __init__(self, tilemapper, roomKey, tiles):
        self.roomKey = roomKey
        self.floor = Floor(tiles)
        self.walls = getWalls()

    def getWalls(self):
        walls = {
        "top": Wall(),
        "bottom": Wall(),
        "left": Wall(),
        "right": Wall()
        }

    ## wouldn't need to do this in c# with a public enum.
        TILE_VOID        = 0 #' '
        TILE_FLOOR       = 1 #'.'
        TILE_WALL        = 2 #'#'
        TILE_CORNER      = 3 #'!'
        TILE_DOOR        = 4 #'+'
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
            
        startTop = self.walls.min.copy()
        startBottom = self.walls.min.copy()

        wallWidth = roomWidth

        push = 0

        while push < roomWidth:
            if startTop.x + push < self.map_width:
                if tilemapper.dmap[startTop.x + push,startTop.y] == TILE_WALL or tilemapper.dmap[startTop.x + push,startTop.y] == TILE_CORNER:
                    startTop = Vector2Int(startTop.x + push,startTop.y)
                    break
                elif tilemapper.dmap[startTop.x + push,startTop.y] == TILE_DOOR:
                    walls["top"].hasDoor = True
                wallWidth -= 1
                push += 1
            else:
                startTop = Vector2Int(startTop.x + push - 1,startTop.y)
                break
            
                
        wallCount = 0
        lastCount = 0
                        
        for j in range(wallWidth):
            if startTop.x + j < self.map_width:
                if wallCount == lastCount:
                    if tilemapper.dmap[startTop.x + j, startTop.y] == TILE_WALL or tilemapper.dmap[startTop.x + j, startTop.y] == TILE_CORNER:
                        walls["top"].segments.append([Vector2Int(startTop.x+j,startTop.y)])
                        tilemapper.dmap[startTop.x+j,startTop.y] = TILE_VISITED
                        wallCount += 1
                else:
                    if tilemapper.dmap[startTop.x + j, startTop.y] == TILE_WALL or tilemapper.dmap[startTop.x + j, startTop.y] == TILE_CORNER:
                        walls["top"].segments[lastCount].append(Vector2Int(startTop.x+j,startTop.y))
                        tilemapper.dmap[startTop.x+j,startTop.y] = TILE_VISITED
                    elif tilemapper.dmap[startTop.x + j,startTop.y] == TILE_DOOR:
                        walls["top"].hasDoor = True
                    else:
                        lastCount += 1
            
        wallWidth = roomWidth

        push = 0

        while push < roomWidth:
            if startBottom.x + push < self.map_width:
                if tilemapper.dmap[startBottom.x + push,startBottom.y] == TILE_WALL or tilemapper.dmap[startBottom.x + push,startBottom.y] == TILE_CORNER:
                    startBottom = Vector2Int(startBottom.x + push,startBottom.y)
                    break
                elif tilemapper.dmap[startBottom.x + push,startBottom.y] == TILE_DOOR:
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
            if startBottom.x + j < self.map_width:
                if wallCount == lastCount:
                    if tilemapper.dmap[startBottom.x + j, startBottom.y] == TILE_WALL or tilemapper.dmap[startBottom.x + j, startBottom.y] == TILE_CORNER:
                        walls["bottom"].segments.append([Vector2Int(startBottom.x+j,startBottom.y)])
                        tilemapper.dmap[startBottom.x+j,startBottom.y] = TILE_VISITED
                        wallCount += 1
                else:
                    if tilemapper.dmap[startBottom.x + j, startBottom.y] == TILE_WALL or tilemapper.dmap[startBottom.x + j, startBottom.y] == TILE_CORNER:
                        walls["bottom"].segments[lastCount].append(Vector2Int(startBottom.x+j,startBottom.y))
                        tilemapper.dmap[startBottom.x+j,startBottom.y] = TILE_VISITED
                    elif tilemapper.dmap[startBottom.x + j,startBottom.y] == TILE_DOOR:
                        walls["bottom"].hasDoor = True
                    else:
                        lastCount += 1

       

        roomHeight = tiles.yMax - tiles.yMin + 3

        walls = self.areas[room].walls

        startLeft = walls["left"].min.copy()
        startRight = walls["right"].min. copy()

        wallHeight = roomHeight

        push = 0

        ##possibly remove tile_corner

        while push < roomHeight:
            if startLeft.y + push < self.map_height:
                if tilemapper.dmap[startLeft.x,startLeft.y + push] == TILE_WALL or tilemapper.dmap[startLeft.x,startLeft.y+ push] == TILE_CORNER:
                    startLeft = Vector2Int(startLeft.x,startLeft.y+push)
                    break
                elif tilemapper.dmap[startLeft.x,startLeft.y+ push] == TILE_DOOR:
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
            if startLeft.y + j < self.map_height:
                if wallCount == lastCount:
                    if tilemapper.dmap[startLeft.x, startLeft.y + j] == TILE_WALL:
                        walls["left"].segments.append([Vector2Int(startLeft.x,startLeft.y + j)])
                        tilemapper.dmap[startLeft.x,startLeft.y + j] = TILE_VISITED
                        wallCount += 1
                else:
                    if tilemapper.dmap[startLeft.x, startLeft.y + j] == TILE_WALL:
                        walls["left"].segments[lastCount].append(Vector2Int(startLeft.x, startLeft.y+j))
                        tilemapper.dmap[startLeft.x, startLeft.y+j] = TILE_VISITED
                    elif tilemapper.dmap[startLeft.x,startLeft.y + j] == TILE_DOOR:
                        walls["left"].hasDoor = True
                    else:
                        lastCount += 1

        wallHeight = roomHeight

        push = 0

        while push < roomHeight:
            if startRight.y + push < self.map_height:
                if tilemapper.dmap[startRight.x,startRight.y+ push] == TILE_WALL or tilemapper.dmap[startRight.x,startRight.y+ push] == TILE_CORNER:
                    startRight = Vector2Int(startRight.x,startRight.y+ push)
                    break
                elif tilemapper.dmap[startRight.x,startRight.y+ push] == TILE_DOOR:
                    walls["right"] = True
                wallHeight -= 1
                push += 1
            else:
                break
        wallCount = 0
        lastCount = 0
            
        ##iterate for second y
            
        for j in range(wallHeight):
            if startRight.y + j < self.map_height:
                if wallCount == lastCount:
                    if tilemapper.dmap[startRight.x, startRight.y + j] == TILE_WALL:
                        walls["right"].segments.append([Vector2Int(startRight.x,startRight.y + j)])
                        tilemapper.dmap[startRight.x,startRight.y + j] = TILE_VISITED
                        wallCount += 1
                else:
                    if tilemapper.dmap[startRight.x, startRight.y + j] == TILE_WALL:
                        walls["right"].segments[lastCount].append(Vector2Int(startRight.x,startRight.y + j))
                        tilemapper.dmap[startRight.x, startRight.y+j] = TILE_VISITED
                    elif tilemapper.dmap[startRight.x,startRight.y + j] == TILE_DOOR:
                        walls["right"].hasDoor = True
                    else:
                        lastCount += 1

        return walls

    def copy():
        return self


class Path(Area):
    def __init__(self):
        self.opensLeft = False
        self.opensRight = False
        self.opensTop = False
        self.opensBottom = False