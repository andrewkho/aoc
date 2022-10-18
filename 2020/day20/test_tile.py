from run import Tile

tile = Tile(['123', '456', '789'])

# up
assert tile.edge(Tile.UP, 0) == "123", tile.edge(Tile.UP, 0)
assert tile.edge(Tile.UP, 1) == "741", tile.edge(Tile.UP, 1)
assert tile.edge(Tile.UP, 2) == "987", tile.edge(Tile.UP, 2)
assert tile.edge(Tile.UP, 3) == "369", tile.edge(Tile.UP, 3)

assert tile.edge(Tile.UP, 4) == "321", tile.edge(Tile.UP, 4) 
assert tile.edge(Tile.UP, 5) == "147", tile.edge(Tile.UP, 5) 
assert tile.edge(Tile.UP, 6) == "789", tile.edge(Tile.UP, 6) 
assert tile.edge(Tile.UP, 7) == "963", tile.edge(Tile.UP, 7) 

#right
assert tile.edge(Tile.RIGHT, 0) == "369", tile.edge(Tile.RIGHT, 0)
assert tile.edge(Tile.RIGHT, 1) == "123", tile.edge(Tile.RIGHT, 1)
assert tile.edge(Tile.RIGHT, 2) == "741", tile.edge(Tile.RIGHT, 2)
assert tile.edge(Tile.RIGHT, 3) == "987", tile.edge(Tile.RIGHT, 3)

assert tile.edge(Tile.RIGHT, 4) == "147", tile.edge(Tile.RIGHT, 4) 
assert tile.edge(Tile.RIGHT, 5) == "789", tile.edge(Tile.RIGHT, 5) 
assert tile.edge(Tile.RIGHT, 6) == "963", tile.edge(Tile.RIGHT, 6) 
assert tile.edge(Tile.RIGHT, 7) == "321", tile.edge(Tile.RIGHT, 7) 

# down
assert tile.edge(Tile.DOWN, 0) == "789", tile.edge(Tile.DOWN, 0)
assert tile.edge(Tile.DOWN, 1) == "963", tile.edge(Tile.DOWN, 1)
assert tile.edge(Tile.DOWN, 2) == "321", tile.edge(Tile.DOWN, 2)
assert tile.edge(Tile.DOWN, 3) == "147", tile.edge(Tile.DOWN, 3)

assert tile.edge(Tile.DOWN, 4) == "987", tile.edge(Tile.DOWN, 4) 
assert tile.edge(Tile.DOWN, 5) == "369", tile.edge(Tile.DOWN, 5) 
assert tile.edge(Tile.DOWN, 6) == "123", tile.edge(Tile.DOWN, 6) 
assert tile.edge(Tile.DOWN, 7) == "741", tile.edge(Tile.DOWN, 7) 

# left
assert tile.edge(Tile.LEFT, 0) == "147", tile.edge(Tile.LEFT, 0)
assert tile.edge(Tile.LEFT, 1) == "789", tile.edge(Tile.LEFT, 1)
assert tile.edge(Tile.LEFT, 2) == "963", tile.edge(Tile.LEFT, 2)
assert tile.edge(Tile.LEFT, 3) == "321", tile.edge(Tile.LEFT, 3)

assert tile.edge(Tile.LEFT, 4) == "369", tile.edge(Tile.LEFT, 4) 
assert tile.edge(Tile.LEFT, 5) == "123", tile.edge(Tile.LEFT, 5) 
assert tile.edge(Tile.LEFT, 6) == "741", tile.edge(Tile.LEFT, 6) 
assert tile.edge(Tile.LEFT, 7) == "987", tile.edge(Tile.LEFT, 7) 

