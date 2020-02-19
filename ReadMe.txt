The code should run with the command 'python Map.py' and should work fine as long as all the files in the map folder are in the directory of the python script so that the code can access them.

I also provide the python notebook which I originally wrote my code in. Executing the cells sequentially should work fine.
For all the paths and tours that the code finds, it asks if you would like to plot the result. Choose y if you have PIL python library installed in your system (can be installed by pip install PIL), and it will plot the result. If you do not have PIL, my code produces Route.txt and Route.txt for all the paths/tours they find. They contain the relevant coordinates in the required format, which can then be used with your own code to plot the path/tour on the Brandeis map image.

For the prim tree and kruskal tree, we notice while running the preorder traversal that the total distance is 57016 feet. Since each edge is traversed twice, this means that the total weight of both the prim and Kruskal trees is 57016/2 = 28508 feet. We also notice that the shortcutting of Prim gives slightly better results, which vary slightly as we change the starting vertex.

We use the following method for shortcutting in pre-order traversal of Prim's minimim spanning tree: 
1. Mark all the vertices as unvisited initially. 
2. Perform the pre-order traversal of Prim's minimum spanning tree while checking the following condition 
3. If the vertex next to current is already marked visited, check if there is a path from the current vertex to the next next vertex and if the distance for that path is smaller than the sum of distances for the paths from current to next+next to next next.
4. If it is indeed smaller, then skip to the next next vertex.

OutputP.txt has the coordinates for plotting Prim's minimum spanning tree
OutputK.txt has the coordinates for plotting Kruskal's minimum spanning tree
OutputPP.txt has the output for pre-order traversal starting at vertex J  of Prim's minimum spanning tree
OutputPS.txt has the output for traversal starting at vertex J of Prim's minimum spanning tree with shortcutting. 
OutputKP.txt has the output for pre-order traversal starting at vertex J  of Kruskal's minimum spanning tree


Remarks:
1. I could not check how to run the code on the COSI lounge computers because they were asking for an account. I applied for an account but the administrator still has not got back to me.
2. Unfortunately, the entire code is submitted as a single file as breaking it into two would require changing all the function names to otherfile.function() in the master code.