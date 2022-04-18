    while came_from[remote_node] is not None:   #loop will stop once we reach the source node (aka node with no parent)
        path.append(came_from[remote_node])     #append the parent of "remote_node" to the path since thats where the remote node came from
        remote_node = came_from[remote_node]    #we increment the remote node by overwriting it with its parent