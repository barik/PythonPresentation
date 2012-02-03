# Remember that A* is also best-first search.
import numpy as np

# A path representation for A*
# Typically, f = g + h is used to determine which path to select, where:
#    g - the cost accumulated thus far in the path
#    h (heuristic) - the estimated distance to the goal
#    f - the path-finding evaluation function
class Path(object):

    def __init__(self, path):
        self.path = path
        self.g = 0
        self.h = 0

    def f(self):
        return self.g + self.h

    # The end of the path is at the end of the list
    # for example,
    #     if the path is A -> B -> C, 
    #     then C is the last element of the list.
    def path_end(self):
        return self.path[-1]

    def __str__(self):
        return "{}, {}, {}".format(self.path, self.g, self.h)

    # The "less-than" operator is used to sort paths using the
    # evaluation function 'f'
    def __lt__(self, other):
        return self.f() < other.f()
    

# Run the graph search algorithm, which will return the
# shortest path to the goal (our heuristic is admissible). 
def go(start, goal, world):

    start_tile = Path([world.getTileForPoint(start)])
    goal_tile = Path([world.getTileForPoint(goal)])

    closed = [] #nodes I have explored - don't want to explore again
    open = [start_tile] #nodes that are candidates for visiting; descending sort

    # When we find a path from start to goal, put it here.
    found = None

    while open:

        # Remove smallest scoring node from open set.
        current = open.pop()

        # You found a path to the goal.  Stop looking!
        if current.path_end() == goal_tile.path_end():
            found = current
            break

        # Add the node (coordinates) to the closed set.
        closed.append(current.path_end())

        expansion = adjacency(current.path_end(), world)
        for e in expansion:

            if e in closed:
                continue

            # Path was not in the closed set.
            expanded_node = Path(current.path + [e])
            expanded_node.h = heuristic(current.path_end(), e)
            expanded_node.g = current.g + 1 #distance is in units of tiles

            open.append(expanded_node)

            pass

        # Sort the nodes from largest to smallest. 
        # A more efficient implementation will use a heap structure.
        open = sorted(open, reverse=True)

    # print "Path: ", found

    return found



# Returns the next move for the path.
#    The first node of the path is where you currently are (index 0)
#    Your next move is therefore index 1 and so on.  If you are already
#    at the destination, or there is no accessible path to the destination,
#    this path returns None.
#
#    Finally, since tiles are much larger than Agents, the path-finding
#    simply targets the center of the tile.
def goNext(found, world):

    if not found:
        return None

    # You're already there. Stay put!
    elif len(found.path) == 1:
        return None

    # Return the tile position.
    else:
        return world.getCenterForTile(found.path[1])


# Return the adjacent tiles, given a tile in the world.
#    For simplicity, we only look at the cardinal directions. (N,S,E,W)
#    As an exercise, try adding diagonal checking!
#
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

# This heuristic uses a straight line as an estimate to the goal.
#    It is admissible, meaning that the actual path will never be shorter than
#    the straight line distance.  In other words, the heuristic does NOT
#    over estimate the distance to the target.
def heuristic(start, end):
    start = np.array(start)
    end = np.array(end)

    return np.sqrt(np.dot(start, end))

if __name__ == 'main':
    pass