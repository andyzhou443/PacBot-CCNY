
I = 1
o = 2
e = 3
O = 4
n = 5
c = 6                        
# Grid enums
# o = normal pellet, e = empty space, O = power pellet, c = cherry position
# I = wall, n = ghost chambers

#       bottom left of pacman board                             # top left of pacman board
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

row = 27
col = 30
print(grid[row][col])

# Direction enums
right = 0
left = 1
up = 2
down = 3

# order of DFS traversal:
dfs_traversal_output = []

def backtrack(stack, travelled):
        print("Start backtracking")
        pos = len(travelled)-2          # Last element of "travelled" without repeating current position
        s_end = len(stack)-1            # Last element of "stack"
        trash = travelled.pop()         # Simply gets rid of current position from "travelled", only time it's used
        back_path = []                  # Logs the backtracking path as they are removed from "travelled"

        while(len(travelled) != 0 and len(stack) != 0):
                if(stack[s_end][0] == travelled[pos][0] + 1) and (stack[s_end][1] == travelled[pos][1]):        # If the last value of "stack" is one position away from the last value in "travelled",
                        back_path.append(travelled.pop())                                                       # Adds pops last value of "travelled" into "back_path",
                        for i in range(0, len(back_path)):                                                      # "back_path" is printed to the terminal (the robot makes these movements)
                                print(back_path[i])

                        travelled.append(back_path[len(back_path) - 1])                                         # Last value of "back_path" added back to "travelled" so it appears in returned list (I now realize this and the last comment is redundent, but the code works and I don't feel like breaking it. Feel free to remove this redundancy)
                        print("Parent!!")
                        print("End backtracking")
                        back_path_dir(back_path,stack)                                                          #passing into a function which figures out the direction of backtracking
                        return travelled

                if(stack[s_end][0] == travelled[pos][0] - 1) and (stack[s_end][1] == travelled[pos][1]):
                        back_path.append(travelled.pop())
                        for i in range(0, len(back_path)):
                                print(back_path[i])

                        travelled.append(back_path[len(back_path) - 1])
                        print("Parent!!")
                        print("End backtracking")
                        back_path_dir(back_path,stack) 
                        return travelled

                if(stack[s_end][0] == travelled[pos][0]) and (stack[s_end][1] == travelled[pos][1] + 1):
                        back_path.append(travelled.pop())
                        for i in range(0, len(back_path)):
                                print(back_path[i])

                        travelled.append(back_path[len(back_path) - 1])
                        print("Parent!!")
                        print("End backtracking")
                        back_path_dir(back_path,stack) 
                        return travelled

                if(stack[s_end][0] == travelled[pos][0]) and (stack[s_end][1] == travelled[pos][1] - 1):
                        back_path.append(travelled.pop())
                        for i in range(0, len(back_path)):
                                print(back_path[i])

                        travelled.append(back_path[len(back_path) - 1])
                        print("Parent!!")
                        print("End backtracking")
                        back_path_dir(back_path,stack)
                        return travelled

                back_path.append(travelled.pop())               # Parent position not found, so last element of "travelled" is moved to "back_path" and "travelled" is checked with "stack" again
                pos = pos - 1                                   # Length of "travelled" changed, so "pos" is accommodated

        if(len(stack) == 0):                                    # If "stack" is empty, there is no more backtracking available, thus all of the pellets are gone (Congrats!!)
                print("All Pellets Eaten :)")
                print()


#Gives direction values to the backktracking solution
def back_path_dir(back_path,stack):

#4 CASES
        print('initial backtrack path:',back_path)
        back_path.reverse()                      #reversing the backtracking path to make it convenient to pop
        last_cell = dfs_traversal_output[-1]     #last cell explored (aka the deadend)  
        back = back_path.pop()

#CASE 1: comparing the first element in back_path to the last visited cell (deadend)

        #checks the location of back relative to deadend

        #left
        if back[0] == last_cell[0] - 1: 
                dfs_traversal_output.append([back[0],back[1],right])
        #right
        if back[0] == last_cell[0] + 1: 
                dfs_traversal_output.append([back[0],back[1],right]) 
        #above
        if back[1] == last_cell[1] + 1: 
                dfs_traversal_output.append([back[0],back[1],right])
        down
        if back[1] == last_cell[1] - 1: 
                dfs_traversal_output.append([back[0],back[1],right])


#CASE 2: comparing the direction of adjacent elements in back_path between the first and last index.
        while len(back_path) > 1:
                back = back_path.pop()
                next = back_path[-1]

                #checks the location of back relative to its adjacent neighbor that's closer to parent cell

                #right
                if back[0] == next[0] - 1: 
                        dfs_traversal_output.append([back[0],back[1],right])
                #left
                if back[0] == next[0] + 1: 
                        dfs_traversal_output.append([back[0],back[1],left])      
                #up
                if back[1] == next[1] + 1: 
                        dfs_traversal_output.append([back[0],back[1],down])
                #down
                if back[1] == next[1] - 1: 
                        dfs_traversal_output.append([back[0],back[1],up])
                print('last element in back', back_path[-1], " length of backpath", len(back_path))


#CASE 3: sometimes we back track by only one cell (which case 1 handles by default)
        if not back_path:
                print('last element in back', back_path, "\nlength of backpath", len(back_path))
                return 


#case 4: compare the direction of the last element on back_path to the parent element that is on the stack (which we have not finished exploring)
        print('last element in back', back_path,"\nlength of backpath", len(back_path))
        back = back_path.pop()
        parent_cell = stack[-1]

        #checks the location of back relative to the parent cell

        #right
        if back[0] == parent_cell[0] - 1:
                dfs_traversal_output.append([back[0],back[1],right])
        #left
        if back[0] == parent_cell[0] + 1:
                dfs_traversal_output.append([back[0],back[1],left])     
        #down
        if back[1] == parent_cell[1] + 1:
                dfs_traversal_output.append([back[0],back[1],down])
        #up
        if back[1] == parent_cell[1] - 1:
                dfs_traversal_output.append([back[0],back[1],up])


        

                
                        

def dfs(x, y, direction):
        print('hello')
        stack = []
        stack.append([x,y,direction])
        value = ""
        current = 0
        travelled = []          # Stores the path of the robot minus the backtracking 

        while(len(stack) != 0):
                current = stack.pop()
                print(current)                  # Moved print of "current" after pop of "stack" for better readability in the terminal
                travelled.append(current)       # Each current point is placed in "travelled"
                legal_moves = 0                 # Keeps track of potential legal moves from current position
                x = current[0]
                y = current[1]
                dfs_traversal_output.append(current)
                value = grid[x][y]
                grid[x][y]=8
                if((x+1<row or y<col) and grid[x+1][y] not in [n, I] and grid[x+1][y] !=8):   #right = 0
                        value = grid[x+1][y]
                        stack.append([x+1,y, right])
                        legal_moves = 1         # If a legal move is found, legal move is set to 1, otherwise legal move is 0

                if((x<row or y+1<col) and grid[x][y+1] not in [n, I] and grid[x][y+1] !=8):   #up = 2
                        value = grid[x][y+1]
                        stack.append([x,y+1, up])
                        legal_moves = 1

                if((x-1>=1 or y>=1) and grid[x-1][y] not in [n, I] and grid[x-1][y] !=8):     #left = 1
                        value = grid[x-1][y]
                        stack.append([x-1,y,left])
                        legal_moves = 1

                if((x>=1 or y-1>=1) and grid[x][y-1] not in [n, I] and grid[x][y-1] !=8):     #down = 3
                        value = grid[x][y-1]
                        stack.append([x,y-1,down])
                        legal_moves = 1

                print(legal_moves)

                if(legal_moves == 0):
                        travelled = backtrack(stack, travelled)         # If a legal move is found, the robot will continue to move, no need to backtrack
                                                                        # If no legal moves are found, the backtracking function will be called
                                                                     # After the backtracking function is finished, the "travelled" list without the backtracked positions replaces the curren "travelled" list

                
                
dfs(14, 7, left)
print('Order of traversal + back tracking:\n', dfs_traversal_output)

f = open("aftergrid.txt", "w")
f.write(str(grid).replace('],','],\n'))
f.close()