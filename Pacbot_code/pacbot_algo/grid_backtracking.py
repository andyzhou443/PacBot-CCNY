
from cmath import sqrt

# Grid enums
# o = normal pellet, e = empty space, O = power pellet, c = cherry position
# I = wall, n = ghost chambers

I = 1
o = 2
e = 3
O = 4
n = 5
c = 6            
# Direction enums
right = 0
left = 1
up = 2
down = 3
         





# GLOBAL VARS
row = 27
col = 30
dfs_traversal_output = [] # to see the road we've walked
x = 14
y = 7
direction = right
parents = {(x, y): (x, y+1, left)}
       

grid = [[I,I,I,I,I,I,I,I,I,I,I,I,e,e,e,e,e,e,e,e,e,I,I,I,I,I,I,I,I,I,I], # 0
        [I,o,o,o,o,I,I,O,o,o,o,I,e,e,e,e,e,e,e,e,e,I,o,o,o,o,o,O,o,o,I],
        [I,o,I,I,o,I,I,o,I,I,o,I,e,e,e,e,e,e,e,e,e,I,o,I,I,o,I,I,I,o,I],
        [I,o,I,I,o,o,o,o,I,I,o,I,e,e,e,e,e,e,e,e,e,I,o,I,I,o,I,e,I,o,I],
        [I,o,I,I,o,I,I,I,I,I,o,I,e,e,e,e,e,e,e,e,e,I,o,I,I,o,I,e,I,o,I],
        [I,o,I,I,o,I,I,I,I,I,o,I,I,I,I,I,I,I,I,I,I,I,o,I,I,o,I,I,I,o,I], # 5
        [I,o,I,I,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,I],
        [I,o,I,I,I,I,I,o,I,I,o,I,I,I,I,I,e,I,I,I,I,I,I,I,I,o,I,I,I,o,I],
        [I,o,I,I,I,I,I,o,I,I,o,I,I,I,I,I,e,I,I,I,I,I,I,I,I,o,I,e,I,o,I],
        [I,o,I,I,o,o,o,o,I,I,o,e,e,e,e,e,e,e,e,e,I,I,o,o,o,o,I,e,I,o,I],
        [I,o,I,I,o,I,I,o,I,I,o,I,I,e,I,I,I,I,I,e,I,I,o,I,I,o,I,e,I,o,I], # 10
        [I,o,I,I,o,I,I,o,I,I,o,I,I,e,I,n,n,n,I,e,I,I,o,I,I,o,I,I,I,o,I],
        [I,o,o,o,o,I,I,o,o,o,o,I,I,e,I,n,n,n,I,e,e,e,o,I,I,o,o,o,o,o,I],
        [I,o,I,I,I,I,I,e,I,I,I,I,I,e,I,n,n,n,n,e,I,I,I,I,I,o,I,I,I,I,I],
        [I,o,I,I,I,I,I,e,I,I,I,I,I,e,I,n,n,n,n,e,I,I,I,I,I,o,I,I,I,I,I], # starting point here
        [I,o,o,o,o,I,I,o,o,o,o,I,I,e,I,n,n,n,I,e,e,e,o,I,I,o,o,o,o,o,I], # 15
        [I,o,I,I,o,I,I,o,I,I,o,I,I,e,I,n,n,n,I,e,I,I,o,I,I,o,I,I,I,o,I],
        [I,o,I,I,o,I,I,o,I,I,o,I,I,e,I,I,I,I,I,e,I,I,o,I,I,o,I,e,I,o,I],
        [I,o,I,I,o,o,o,o,I,I,o,e,e,e,e,e,e,e,e,e,I,I,o,o,o,o,I,e,I,o,I],
        [I,o,I,I,I,I,I,o,I,I,o,I,I,I,I,I,e,I,I,I,I,I,I,I,I,o,I,e,I,o,I],
        [I,o,I,I,I,I,I,o,I,I,o,I,I,I,I,I,e,I,I,I,I,I,I,I,I,o,I,I,I,o,I], # 20
        [I,o,I,I,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,I],
        [I,o,I,I,o,I,I,I,I,I,o,I,I,I,I,I,I,I,I,I,I,I,o,I,I,o,I,I,I,o,I],
        [I,o,I,I,o,I,I,I,I,I,o,I,e,e,e,e,e,e,e,e,e,I,o,I,I,o,I,e,I,o,I],
        [I,o,I,I,o,o,o,o,I,I,o,I,e,e,e,e,e,e,e,e,e,I,o,I,I,o,I,e,I,o,I],
        [I,o,I,I,o,I,I,o,I,I,o,I,e,e,e,e,e,e,e,e,e,I,o,I,I,o,I,I,I,o,I], # 25
        [I,o,o,o,o,I,I,O,o,o,o,I,e,e,e,e,e,e,e,e,e,I,o,o,o,o,o,O,o,o,I],
        [I,I,I,I,I,I,I,I,I,I,I,I,e,e,e,e,e,e,e,e,e,I,I,I,I,I,I,I,I,I,I]]
#        |         |         |         |         |         |         |   top right of pacman board
#        0         5        10        15       20         25       30


# for debugging reasons to see grid changing in real time
f = open("aftergrid.txt", "w")
f.write(str(grid).replace('],','],\n'))
f.close() 
stack = []
stack.append([x,y,direction])

# allows us to add the surrounding nodes to the stack when either going one path or backtracking
def addnodes(x, y):
        if((x+1<row or y<col) and grid[x+1][y] not in [n, I] and grid[x+1][y] !=8):   #right = 0
                stack.append([x+1,y, right])
                parents[(x+1, y)] = (x, y, left)

        if((x<row or y+1<col) and grid[x][y+1] not in [n, I] and grid[x][y+1] !=8):   #up = 2
                stack.append([x,y+1, up])
                parents[(x, y+1)] = (x, y, down)

        if((x-1>=1 or y>=1) and grid[x-1][y] not in [n, I] and grid[x-1][y] !=8):     #left = 1
                stack.append([x-1,y,left])
                parents[(x-1, y)] = (x, y, right)

        if((x>=1 or y-1>=1) and grid[x][y-1] not in [n, I] and grid[x][y-1] !=8):     #down = 3
                stack.append([x,y-1,down])
                parents[(x, y-1)] = (x, y, up)
        


def dfs(x, y, direction):
        current = 0
        previous = [14,8,0] # adding a dummy var that way our first check for distance is true
        while(len(stack) != 0):
                current = stack.pop()
                print(f"current: {current}\tprevious: {previous}")                  # Moved print of "current" after pop of "stack" for better readability in the terminal
                x = current[0]
                y = current[1]
                # updating grid real time
                f = open("aftergrid.txt", "w")
                f.write(str(grid).replace('],','],\n'))
                f.close()
                # if the distance is greater than 1 we have to backtrack 
                if (sqrt((previous[0] - x) **2 + (previous[1] - y )**2) == 1 ): # distance formula
                        dfs_traversal_output.append(current)
                        grid[x][y]=8
                        addnodes(x,y)
                        previous = [x, y, direction]
                else:
                        # storing old variable as we are changing the current node
                        old_curr = current
                        print(f"we are at {current}, must backtrack to {previous}")
                        print(f"the parent of {current} is {list(parents[(x, y)])}")
                        # if the distance is not 1, keep backtracking
                        while(sqrt((old_curr[0] - previous[0])**2 + (previous[1] - old_curr[1])**2) != 1):
                                # get the parent of the current node 
                               current = list(parents[(previous[0], previous[1])])
                               # add it to the path list
                               dfs_traversal_output.append(current)
                               # update the previous node
                               previous = current
                               # search for neighbors while backtracking
                               addnodes(current[0], current[1])

                
def old_dfs(x, y, direction):
        current = 0
        previous = [14,8,0] # adding a dummy var that way our first xor is true
        while(len(stack) != 0):
                current = stack.pop()
                print(f"current: {current}\tprevious: {previous}")                  # Moved print of "current" after pop of "stack" for better readability in the terminal
                x = current[0]
                y = current[1]
                # dfs_traversal_output.append(current)
                grid[x][y]=8
                f = open("aftergrid.txt", "w")
                f.write(str(grid).replace('],','],\n'))
                f.close()
                if((x+1<row or y<col) and grid[x+1][y] not in [n, I] and grid[x+1][y] != 8):   #right = 0
                        dfs_traversal_output.append(current)
                        stack.append([x+1,y, right])
                        parents[(x+1, y)] = (x, y, left)

                if((x<row or y+1<col) and grid[x][y+1] not in [n, I] and grid[x][y+1] != 8):   #up = 2
                        dfs_traversal_output.append(current)

                        stack.append([x,y+1, up])
                        parents[(x, y+1)] = (x, y, down)

                if((x-1>=1 or y>=1) and grid[x-1][y] not in [n, I] and grid[x-1][y] != 8):     #left = 1
                        dfs_traversal_output.append(current)

                        stack.append([x-1,y,left])
                        parents[(x-1, y)] = (x, y, right)

                if((x>=1 or y-1>=1) and grid[x][y-1] not in [n, I] and grid[x][y-1] != 8):     #down = 3
                        dfs_traversal_output.append(current)

                        stack.append([x,y-1,down])
                        parents[(x, y-1)] = (x, y, up)
        
def main():               
        
        dfs(x, y, right)
        # print('Order of traversal + back tracking:\n', dfs_traversal_output)

       

        f = open("road.txt", "w")
        f.write(str(dfs_traversal_output).replace('],','],\n'))
        f.close()
        


if __name__ == "__main__":
    main()
