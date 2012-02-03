# Remember that A* is also best-first search.
import heapq
import numpy as np

# A nice node wrapper for A-Star
class Node(object):

    def __init__(self, path):
        self.path = path
        self.g = 0
        self.h = 0

    def f(self):
        return self.g + self.h

    def path_end(self):
        return self.path[-1]

    def __str__(self):
        return "{}, {}, {}".format(self.path, self.g, self.h)

    def __cmp__(self, other):
        # TODO
        return 0

# Run the graph search algorithm, which will return the
# next tile to go to. Simplify bot so that it only
# goes to the center of the tiles.
def go(start, goal, world):

    start_tile = Node([world.getTileForPoint(start)])
    goal_tile = Node([world.getTileForPoint(goal)])

    closed = []
    open = [start_tile]

    # When we find a path from start to goal, put it here.
    found = None

    while open:

        # Remove node from open set.
        current = open.pop()

        if current.path_end() == goal_tile.path_end():
            found = current
            break

        # Add the node (coordinates) to the closed set.
        closed.append(current.path_end())

        expansion = adjacency(current.path_end(), world)
        for e in expansion:

            if e in closed:
                continue

            # Node was not in the closed set.
            expanded_node = Node(current.path + [e])
            expanded_node.h = heuristic(current.path_end(), e)
            expanded_node.g = current.g + 1

            open.append(expanded_node)

            pass

        # Sort the nodes from largest to smallest. Fix the __cmp__
        # function.
        open.sort()
        open.reverse()

    print "Path: ", found

    # Oops, no way to get from point A to point B. Stay put.
    if not found:
        return None

    # You're already there. Stay put?
    elif len(found.path) == 1:
        return None

    # Return the tile position.
    else:
        return world.getCenterForTile(found.path[1])

# Return the adjacent tiles for this world.
def adjacency(tile, world):

    rows = len(world.level)
    cols = len(world.level[0])

    tile_x = int(tile[0])
    tile_y = int(tile[1])

    adj = []

    # Check the four surrounding tiles, if they are accessible, then
    # add them to the adjacency list.

    if tile_y + 1 < cols and not world.isWallAtTile((tile_x, tile_y + 1)):
        adj.append((tile_x, tile_y + 1))
    if tile_y - 1 >= 0 and not world.isWallAtTile((tile_x, tile_y - 1)):
        adj.append((tile_x, tile_y - 1))
    if tile_x + 1 < rows and not world.isWallAtTile((tile_x + 1, tile_y)):
        adj.append(((tile_x + 1, tile_y)))
    if tile_x - 1 >= 0 and not world.isWallAtTile((tile_x - 1, tile_y)):
        adj.append(((tile_x - 1, tile_y)))

    return adj

def heuristic(start, end):
    start = np.array(start)
    end = np.array(end)

    return np.sqrt(np.dot(start, end))

if __name__ == 'main':
    pass