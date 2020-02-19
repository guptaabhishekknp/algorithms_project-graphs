#!/usr/bin/env python
# coding: utf-8

# In[1]:


import math
import sys


# In[2]:


#functions for heap data structure
#adjacency lists are implemented as python dictionaries

def PARENT(i,D):
    n = len(D)
    if i>0:
        return math.floor((i-1)/2) 
    else:
        return -1

def LCHILD(i,D):
    n = len(D)
    if ((2*i)+1) < n:
        return (2*i)+1 
    else:
        return -1

def RCHILD(i,D):
    n = len(D)
    if ((2*i)+2) < n:
        return (2*i)+2 
    else:
        return -1

def RSIB(i,D):
    n = len(D)
    if i<(n-1) and i%2 == 1:
        return i+1
    else:
        return -1

def PERC_UP(i,D):
    while i>0 and D[i][1]<D[PARENT(i,D)][1]:
        p = D[i] 
        D[i] = D[PARENT(i,D)]
        D[PARENT(i,D)] = p
        i = PARENT(i,D)
    return D

def INSERT(v,D):
    n = len(D)
    D.insert(n,v)
    PERC_UP(n,D)
    return D

def PERCDOWN(i,D):
    while (RCHILD(i,D)!=-1 and D[i][1]>D[RCHILD(i,D)][1]) or (LCHILD(i,D)!=-1 and D[i][1]>D[LCHILD(i,D)][1]):
        if RCHILD(i,D)==-1:
            j = LCHILD(i,D)
        elif LCHILD(i,D)==-1:
            j = RCHILD(i,D)
        else: 
            j = RCHILD(i,D)
            if D[LCHILD(i,D)][1]<D[RCHILD(i,D)][1]:
                j = LCHILD(i,D)
        
        p = D[i]
        D[i] = D[j]
        D[j] = p
        i = j        
    return D

def DELETEMIN(D):
    n = len(D)-1
    smallest = D[0]
    D[0]=D[n]
    del D[n]
    D = PERCDOWN(0,D)
    return D, smallest

def DECREASE(i,new_value,D):
    D[i] = (D[i][0],new_value)
    D = PERC_UP(i,D)
    return D


# In[3]:


def initialize_D(start_vertex, graph):
    infty = float("inf") #infinity value, change this to 10,000 before submitting the code
    vertices = [key for key in graph]
    start_vertex_ngbrs = graph[start_vertex]
    D = [(start_vertex,0)]
    vertices.remove(start_vertex)    
    #if you want to uncomment the 3 lines below, the back pointer must be initialized 
    #so that vertices adjacent to the starting vertex point to the starting vertex
    #for nghbr in start_vertex_ngbrs: 
    #    D = INSERT((nghbr[0],nghbr[1]),D)
    #    vertices.remove(nghbr[0])    
    for v in vertices:
        D = INSERT((v,infty),D)        
    return D

def index_in_list(vert_indx,D):
    i = 0
    for v in D:
        if v[0] == vert_indx:
            return i
        i+=1
    return -1

def print_paths(graph, start_vertex, back_pointer):
    for key in graph:
        l = []
        k = key
        while k != back_pointer[k]:
            l.append(k)
            k = back_pointer[k]            
        l.append(start_vertex)
        l = l[::-1]
        print('path from {} to {} is given by:'.format(start_vertex,key),l)
        print('total cost of this path is:',find_path_length(l,graph))
    return

def find_path_length(l,graph):
    length = 0
    for i in range(len(l)-1):
        idx = index_in_list(l[i+1],graph[l[i]])        
        length+= graph[l[i]][idx][1]
        
    return length

def run_Dijkstras(start_vertex, graph):
    back_pointer = {key:key for key in graph}
    mark = {key:0 for key in graph} #0 for unmarked, 1 for marked

    D = initialize_D(start_vertex, graph)

    #for strt_nbrs in graph[start_vertex]:
    #    back_pointer[strt_nbrs[0]] = start_vertex

    while 0 in list(mark.values()):
        D, v = DELETEMIN(D)
        current_vertex = v[0]
        mark[current_vertex] = 1
        for adj_vert in graph[current_vertex]:
            adj_indx = adj_vert[0]
            adj_cost = adj_vert[1]
            j = index_in_list(adj_indx,D)
            if mark[adj_indx] == 0 and D[j][1]>v[1]+adj_cost:
                D = DECREASE(j,v[1]+adj_cost,D)
                back_pointer[adj_indx] = current_vertex
    
    return back_pointer

def words_in_name(lst):
    new_list = []
    for piece in lst:
        word = piece.rstrip('&"\/').lstrip('&"\/').split('-')
        if len(word[0]) > 0:
            new_list = new_list+word            
    return new_list


def create_vertex_data():
    vertex_data = read_from_file("MapDataVertices.txt")
    for element in vertex_data:
        element[2] = int(element[2])
        element[3] = int(element[3])
        #element[4] = element[4]#.split()#words_in_name(element[4].split())
    return vertex_data      #returns a list of tuples: 
                            #(vertex_id,label,x-coordinate,y-coordinate,name,list of words in the name)

def read_from_file(filename):
    data = []
    with open(filename) as f:
        for line in f:
            fields = line.split('"')[0].split()
            
            if fields!=[] and fields[0][0]!='/':
                name = line.split('"')[1]
                data.append([int(fields[0])]+fields[1:]+[name])
    return data

def create_edge_data():    
    edge_data = read_from_file("MapDataEdges.txt")
    for element in edge_data:
        element[3] = int(element[3])
        element[4] = int(element[4])
        element[5] = int(element[5])
        element[6] = int(element[6])
        element[8] = element[8].strip('()')
    return edge_data

def construct_graph(vertex_data, edge_data, has_skateboard, minimize_time):
    
    graph = {vertex[0]:[] for vertex in vertex_data}
    for edge in edge_data:
        if minimize_time:
            cost = calculate_time(edge[5],has_skateboard,edge[8])
        else:
            cost = edge[5]
        
        graph[edge[3]].append(
            (edge[4],
             cost,
             edge[0]
            )
        )
    
    return graph

def make_path(graph, start_vertex, end_vertex, back_pointer, edge_data, has_skateboard):
    l = []
    while end_vertex != back_pointer[end_vertex]:
        l.append(end_vertex)
        end_vertex = back_pointer[end_vertex]            
    l.append(start_vertex)
    l = l[::-1]
    return l

def create_output(l, graph, edge_data, has_skateboard):
    time = 0
    distance = 0
    legs = 0
    path_list = []
    
    for i in range(len(l)-1):
        v = l[i]
        j = index_in_list(l[i+1],graph[l[i]])
        edge_indx = graph[l[i]][j][2]
        
        dist_for_leg = edge_data[find_index_in_edge_data(edge_indx,edge_data)][5]
        time_for_leg = calculate_time(dist_for_leg,has_skateboard,edge_data[find_index_in_edge_data(edge_indx,edge_data)][8])
        time += time_for_leg
        distance += dist_for_leg
        legs += 1 
        path_list.append('FROM: ({}) {}\n'.format(vertex_data[l[i]][1],vertex_data[l[i]][-1]))
        path_list.append('ON: {}\n'.format(edge_data[find_index_in_edge_data(edge_indx,edge_data)][-1]))
        path_list.append('Travel {} feet in direction {} degrees {}\n'.format(dist_for_leg,edge_data[find_index_in_edge_data(edge_indx,edge_data)][-4],edge_data[find_index_in_edge_data(edge_indx,edge_data)][-3]))
        path_list.append('TO: ({}) {}\n'.format(vertex_data[l[i+1]][1],vertex_data[l[i+1]][-1]))
        path_list.append('({} seconds)\n\n'.format(time_for_leg))
    path_list.append('legs = {}, distance = {} feet, time = {} seconds\n'.format(legs,distance,time))
    return ''.join(path_list)

def calculate_time(edge_length, has_skateboard, C):

    WalkSpeed = 272    #ft/min = (3.1 miles/hr) * (5280 ft/mile) / (60 mins/hr)
    WalkFactorU = 0.9  #Multiply walk speed by this for walk up.
    WalkFactorD = 1.1  #Multiply walk speed by this for walk down.
    SkateFactorU = 1.1 #Multiply walk speed by this for skateboard up.
    SkateFactorF = 2.0 #Multiply walk speed by this for skateboard flat.
    SkateFactorD = 5.0 #Multiply walk speed by this for skateboard down.
    StepFactorU = 0.5  #Multiply walk speed by this for walk up steps.
    StepFactorD = 0.9  #Multiply walk speed by this for walk down steps.
    BridgeFactor = 1.0 #Multiply walk speed by this for walking on a bridge.

    div_factor = {
        'f': 1,          
        'x': (int(has_skateboard)*SkateFactorF + (int(not has_skateboard))*1),
        'F': int(has_skateboard)*SkateFactorF + (int(not has_skateboard))*1,
        'u': WalkFactorU,
        'U': int(has_skateboard)*SkateFactorU + (int(not has_skateboard))*WalkFactorU,
        'd': WalkFactorD,
        'D': int(has_skateboard)*SkateFactorD + (int(not has_skateboard))*WalkFactorD,
        's': StepFactorU,
        't': StepFactorD,
        'b': BridgeFactor                             
        }
    
    t = int(60*float(edge_length)/float(WalkSpeed) + 0.5) 
    t /= div_factor[C]

    return int(t)

def create_route_file(l, vertex_data):
    MapWidthFeet = 5521 
    MapHeightFeet = 4369 
    MapWidthPixels = 2528 
    MapHeightPixels = 2000 
    CropLeft = 150 
    CropDown = 125 
    file = open(r"Route.txt","w+") 
    file_cropped = open(r"RouteCropped.txt","w+")
    for i in range(len(l)-1):
        v = vertex_data[find_index_in_edge_data(l[i],vertex_data)][2]
        w = vertex_data[find_index_in_edge_data(l[i],vertex_data)][3]
        x = vertex_data[find_index_in_edge_data(l[i+1],vertex_data)][2]
        y = vertex_data[find_index_in_edge_data(l[i+1],vertex_data)][3]
        a = int(v * MapHeightPixels / MapHeightFeet)
        b = int(w * MapWidthPixels / MapWidthFeet)
        c = int(x * MapHeightPixels / MapHeightFeet)
        d = int(y * MapWidthPixels / MapWidthFeet)
        file.write('{} {} {} {}\n'.format(a,b,c,d))
        a = a - CropLeft
        b = b - CropDown
        c = c - CropLeft
        d = d - CropDown
        file_cropped.write('{} {} {} {}\n'.format(a,b,c,d))
    file.close()    
    file_cropped.close()    
    return

def plot_on_map():
    from PIL import Image, ImageDraw
    img = Image.open('BrandeisMapLabeled.jpg')
    drawing = ImageDraw.Draw(img)
    with open('Route.txt') as f:
        for line in f:
            coords = line.split()
            a, b, c, d = int(coords[0]), int(coords[1]), int(coords[2]), int(coords[3])
            drawing.line([(a,b),(c,d)],fill='pink',width=15)        
    img.show()
    return

def print_list(l):
    for i in l:
        print('*',i)
    return 

def get_vertex_id(s, vertex_data): #get vertex id from the input string s
    l = []
    for data in vertex_data:
        if s.lower() == data[1].lower():
            return data[0]
        if s.lower() == data[4].lower():
            return data[0]
        
        if s.lower() in data[4].lower():
            l.append(data[0])
        
    if len(l)==1:
        return l[0]
    if len(l)>1:
        print('Ambigous name. Following multiple matches found.\n')
        print_list([vertex_data[i][4] for i in l])
        print('\nPlease enter a substring that uniquely identifies the place.\n')
        return 0
    if len(l)==0:
        print('Place not found. Try again.')
        return 0

#the string entered should be either the map location, for example L24 etc, or, a substring of a unique name 
#so either the full name or a word that uniquely identifies the location for example 'farber', 'Farber l', 'Farber lib'
#are all substrings of unique location 'Farber Library'

#not case sensitive so more flexible
#    return -1 #location not found, try again
#    return -2 #more than one location for example 'schwartz will give two locations', 'Hassenfeld Lot will give two locations'

#maybe just return a single location error and try again- NO!!! the 
#first check if it matches map location
#then check if it is exactly the name of a place
#then check if it is substring


# # Part 2
# # Part 2
# # Part 2
# # Part 2
# # Part 2
# # Part 2
# # Part 2
# # Part 2
# # Part 2
# # Part 2
# # Part 2
# # Part 2
# # Part 2
# # Part 2
# # Part 2
# # Part 2


def is_undirected(graph): #checks if every edge - reverse-edge pair has the same weight, 
                          #so that the graph represented by adjacency list can be interpreted as undirected
    result = True
    for key in graph:
        for vert in graph[key]:
            vertex_indx = vert[0]
            edge_wt = vert[1]
            j = index_in_list(key, graph[vertex_indx])
            reverse_edge_wt = graph[vertex_indx][j][1]
            if edge_wt!=reverse_edge_wt:
                print(key,vertex_indx,edge_wt,j,reverse_edge_wt)
                result = False
    return result
def just_one(a, b, l):
    return ((a in l) and (b not in l)) or ((a not in l) and (b in l))

def find_index_in_edge_data(idx,edge_data):
    l = [x[0] for x in edge_data]
    return l.index(idx)

def min_span_tree(graph, start_vertex, edge_data):
    T = set()
    to_put_back = []
    vertices_in_T = set()
    vertices_in_T.add(start_vertex)
    
    edge_cost_pairs = set()
    for key in graph:
        for element in graph[key]:
            edge_cost_pairs.add((element[2],element[1]))
    heap = []
    
    for x in list(edge_cost_pairs):
        heap = INSERT(x,heap)
    
    num_vertices = len(graph)
    while len(T)<num_vertices-1:
        heap, smallest = DELETEMIN(heap)
        smallest = smallest[0]
        indx_sm_edge_data = find_index_in_edge_data(smallest,edge_data)
        
        while not just_one(edge_data[indx_sm_edge_data][3],edge_data[indx_sm_edge_data][4],vertices_in_T): #loop until there is a edge with exactly one 
            to_put_back.append(smallest)
            
            #print(heap)
            #print(len(vertices_in_T))
            heap, smallest = DELETEMIN(heap)
            
            smallest = smallest[0]
            indx_sm_edge_data = find_index_in_edge_data(smallest,edge_data)
        T.add(smallest)
        vertices_in_T.add(edge_data[indx_sm_edge_data][3])
        vertices_in_T.add(edge_data[indx_sm_edge_data][4])
        for edg in to_put_back:
            heap = INSERT((edg,edge_data[find_index_in_edge_data(edg,edge_data)][5]),heap)
        to_put_back = []
        
    return T

def plot_edges(edge_list, edge_data, vertex_data):#needs to be changed!!!!!!!!
    MapWidthFeet = 5521 
    MapHeightFeet = 4369 
    MapWidthPixels = 2528 
    MapHeightPixels = 2000
    img = Image.open('BrandeisMapLabeled.jpg')
    drawing = ImageDraw.Draw(img)
    for edg in edge_list:
        v_1 = edge_data[edg][3]
        v_2 = edge_data[edg][4]
        v = vertex_data[v_1][2]
        w = vertex_data[v_1][3]
        x = vertex_data[v_2][2]
        y = vertex_data[v_2][3]
        a = int(v * MapHeightPixels / MapHeightFeet)
        b = int(w * MapWidthPixels / MapWidthFeet)
        c = int(x * MapHeightPixels / MapHeightFeet)
        d = int(y * MapWidthPixels / MapWidthFeet)
        drawing.line([(a,b),(c,d)],fill='pink',width=10)  
        
    img.show()
    return

def plotting_cordinates_from_edges(edge_list, edge_data, vertex_data):
    MapWidthFeet = 5521 
    MapHeightFeet = 4369 
    MapWidthPixels = 2528 
    MapHeightPixels = 2000
    coords = []
    for edg in edge_list:
        v_1 = edge_data[find_index_in_edge_data(edg,edge_data)][3]
        v_2 = edge_data[find_index_in_edge_data(edg,edge_data)][4]
        v = vertex_data[v_1][2]
        w = vertex_data[v_1][3]
        x = vertex_data[v_2][2]
        y = vertex_data[v_2][3]
        a = int(v * MapHeightPixels / MapHeightFeet)
        b = int(w * MapWidthPixels / MapWidthFeet)
        c = int(x * MapHeightPixels / MapHeightFeet)
        d = int(y * MapWidthPixels / MapWidthFeet)
        coords.append(str(a)+' '+str(b)+' '+str(c)+' '+str(d))
        
    
    return '\n'.join(coords)

def tree_from_edges(edges,  vertex_data, edge_data):
    
    tree = {key[0]: set() for key in vertex_data}
    
    for edge in edges:
        edge_idx = find_index_in_edge_data(edge,edge_data)
        v1 = edge_data[edge_idx][3]
        v2 = edge_data[edge_idx][4]
        tree[v1].add((v2,0))#0 is a dummy coordinate in the tuple
        tree[v2].add((v1,0))#0 is a dummy coordinate in the tuple
        
    for key in tree:
        tree[key] = list(tree[key])
    return tree
        
def plot_traversal(traversal,  vertex_data):#needs to be changed!!!!!!!!
    from PIL import Image, ImageDraw
    MapWidthFeet = 5521 
    MapHeightFeet = 4369 
    MapWidthPixels = 2528 
    MapHeightPixels = 2000
    img = Image.open('BrandeisMapLabeled.jpg')
    drawing = ImageDraw.Draw(img)
    visited = []
    for i in range(len(traversal)-1):
        
        v_1 = traversal[i]
        v_2 = traversal[i+1]
        visited.append(v_1)
        v = vertex_data[v_1][2]
        w = vertex_data[v_1][3]
        x = vertex_data[v_2][2]
        y = vertex_data[v_2][3]
        a = int(v * MapHeightPixels / MapHeightFeet)
        b = int(w * MapWidthPixels / MapWidthFeet)
        c = int(x * MapHeightPixels / MapHeightFeet)
        d = int(y * MapWidthPixels / MapWidthFeet)
        drawing.line([(a,b),(c,d)],fill='pink',width=10)  
        
        if v_2 in visited:
            drawing.line([(a,b),(c,d)],fill='red',width=2)  
        else:
            drawing.line([(a,b),(c,d)],fill='pink',width=10)  
        
    img.show()
    return

def pre_order_trvsl(tree, root_key, vistd_vrtx_list):#returns a list of vertices in the order in which they are traversed
    vistd_vrtx_list.append(root_key)
    for nghbr in tree[root_key]:
        if nghbr[0] not in vistd_vrtx_list:
        
            vistd_vrtx_list = pre_order_trvsl(tree,nghbr[0],vistd_vrtx_list)
            
        if vistd_vrtx_list[-1]!=root_key:
            vistd_vrtx_list.append(root_key)    
    return vistd_vrtx_list

def find_cost(a,b, graph):
    for e in graph[a]:
        if b==e[0]:
            return e[1]
    return float("inf")

#if the next vertex is already visited, look two places ahead and if there's a path to that and the distance through that parth is shorter
#(yes, this needs to be checked as it is not always true) then shortcut it.T
def prim_shortchut_traversal(traversal, graph):
    visited = [traversal[0]]
    i = 0
    while i < len(traversal)-2:
        v_1 = traversal[i]
        v_2 = traversal[i+1]
        v_3 = traversal[i+2]
        
        #if find_cost(v_1,v_3, graph)<float("inf"):#if there is any edge at all shortcut it
        if (find_cost(v_1,v_3, graph)<find_cost(v_1,v_2, graph)+find_cost(v_2,v_3, graph)) and (v_2 in visited):#shortcut only if the new edge is better
            visited.append(v_3)
            i+=2
        else:
            visited.append(v_2)
            i+=1
    return visited

#a dict with keys as vertices and values as an index of set, which is initially all different but set same for unioning 2 sets
def kruskal_min_spanning_tree(edge_data, vertex_data, graph):
    vertex_sets_indices = {key[0]:key[0] for key in vertex_data}#assign all set indices as distinct
    T = set()
    edge_cost_pairs = set()
    for key in graph:
        for element in graph[key]:
            edge_cost_pairs.add((element[2],element[1]))
    heap = []
    for x in list(edge_cost_pairs):
        heap = INSERT(x,heap)
    n_vert = len(vertex_data)
    while len(T)<n_vert-1:
        to_put_back = []
        while True:
            heap, smallest = DELETEMIN(heap)
            smallest = smallest[0]
            indx_sm_edge_data = find_index_in_edge_data(smallest,edge_data)
            v_1 = edge_data[indx_sm_edge_data][3]
            v_2 = edge_data[indx_sm_edge_data][4]
            if vertex_sets_indices[v_1]!=vertex_sets_indices[v_2]:
                T.add(smallest)
                n1 = vertex_sets_indices[v_1]
                n2 = vertex_sets_indices[v_2]
                n = max([n1,n2])
                for key in vertex_sets_indices:
                    if vertex_sets_indices[key]==n1 or vertex_sets_indices[key]==n2:
                        vertex_sets_indices[key]=n
                for edg in to_put_back:
                    heap = INSERT((edg,edge_data[find_index_in_edge_data(edg,edge_data)][5]),heap)
                    
                break
            else:
                
                to_put_back.append(smallest)
    return T

def prim_preorder(start_vertex, vertex_data, edge_data):
    graph_new = construct_graph(vertex_data[5:], edge_data[20:], False, False) #delete the black hole and corners vertices and edges
    min_tree_edges = min_span_tree(graph_new, start_vertex, edge_data[20:])
    prim_min_spanning_tree = tree_from_edges(min_tree_edges, vertex_data[5:], edge_data[20:])    
    traversal = pre_order_trvsl(prim_min_spanning_tree, start_vertex, [])
    output = create_output(traversal,graph_new,edge_data[20:], False)
    print('Would you like to plot the result from Route.txt into the brandeis map? (Requires the python package PIL to be installed)')
    print('y/n - default n? ')
    plot = input()
    print(output)
    create_route_file(traversal,vertex_data)
    
    if plot.lower() == 'y':
        plot_on_map()
    #plot_traversal(traversal, vertex_data)
    
    #plot_traversal(traversal, vertex_data)
    
    
    return output, traversal

def prim_shortcut(start_vertex, vertex_data, edge_data):
    graph_new = construct_graph(vertex_data[5:], edge_data[20:], False, False) #delete the black hole and corners vertices and edges
    min_tree_edges = min_span_tree(graph_new, start_vertex, edge_data[20:])
    prim_min_spanning_tree = tree_from_edges(min_tree_edges, vertex_data[5:], edge_data[20:])
    traversal = pre_order_trvsl(prim_min_spanning_tree, start_vertex, [])    
    prim_shortcut_trav = prim_shortchut_traversal(traversal, graph_new)
    output = create_output(prim_shortcut_trav,graph_new,edge_data[20:], False)
    print('Would you like to plot the traversal onto the brandeis map? (Requires the python package PIL to be installed)')
    print('y/n - default n? ')
    plot = input()
    print(output)
    create_route_file(prim_shortcut_trav,vertex_data)
    
    if plot.lower() == 'y':
        plot_on_map()
    #plot_traversal(traversal, vertex_data)
    
    #plot_traversal(prim_shortcut_trav, vertex_data)
    return output, prim_shortcut_trav

def kruskal_preorder(start_vertex, vertex_data, edge_data):
    graph_new = construct_graph(vertex_data[5:], edge_data[20:], False, False) #delete the black hole and corners vertices and edges
    kruskal_edges = kruskal_min_spanning_tree(edge_data[20:],vertex_data[5:], graph_new)
    k_min_spanning_tree = tree_from_edges(kruskal_edges, vertex_data[5:], edge_data[20:])
    traversal = pre_order_trvsl(k_min_spanning_tree, start_vertex, [])
    output = create_output(traversal,graph_new,edge_data[20:], False)
    print('Would you like to plot the traversal onto the brandeis map? (Requires the python package PIL to be installed)')
    print('y/n - default n? ')
    plot = input()
    print(output)
    create_route_file(traversal,vertex_data)
    
    if plot.lower() == 'y':
        plot_on_map()
    #plot_traversal(traversal, vertex_data)
    return output, traversal

def tour(start_vertex, vertex_data, edge_data):
    print('Enter one of these tour options:')
    print('    0: Preorder traversal of Prim tree')
    print('    1: Triangle shorcuts of Prim traversal')
    print('    2: Preorder traversal of Kruskal tree')
    print('    or return to quit')
    option = input()
    if option == '0':
        prim_preorder(start_vertex, vertex_data, edge_data)
    elif option == '1':
        prim_shortcut(start_vertex, vertex_data, edge_data)
    elif option == '2':        
        kruskal_preorder(start_vertex, vertex_data, edge_data)
    elif option == '':
        sys.exit('You pressed return')
    else:
        print('Enter valid option')
        tour(start_vertex)
    return


# In[9]:


def find_path(start_vertex, end_vertex, vertex_data, edge_data, has_skateboard, minimize_time):
    graph = construct_graph(vertex_data, edge_data, has_skateboard, minimize_time)
    back_pointer = run_Dijkstras(start_vertex,graph)
    l = make_path(graph, start_vertex, end_vertex, back_pointer, edge_data, has_skateboard)
    output = create_output(l, graph, edge_data, has_skateboard)
    
    return l, output


def run_map(vertex_data, edge_data):
    print("******************************WELCOME TO THE BRANDEIS MAP******************************\n")
    print('Entered locations may be: \nthe map location(eg L1, U22 etc) or, \nthe exact name (farber library etc), or, \na substring that uniqiely identifies the place (eg., farber l etc)\n')

    got_location = False
    while got_location == False:
        print('Enter start (return to quit):')
        inp = input()
        if inp == '':
            sys.exit('You pressed return.')
        start_vertex = get_vertex_id(inp,vertex_data)
        if start_vertex!=0:
            got_location = True


    got_location = False
    while got_location == False:
        print('Enter finish (or return to do a tour):')
        inp = input()
        if inp == '':
            tour(start_vertex, vertex_data, edge_data)
            sys.exit()
        end_vertex = get_vertex_id(inp,vertex_data)

        if end_vertex!=0:
            got_location = True


    print('Have a skateboard (y/n - default=n)?')
    sk = input()
    print('Minimize time (y/n - default=n)?')
    ti = input()



    #t f
    has_skateboard = False
    minimize_time = False
    if sk.lower() == 'y':
        has_skateboard = True
    if ti.lower() == 'y':
        minimize_time = True

    path_list, output = find_path(start_vertex, end_vertex, vertex_data, edge_data, has_skateboard, minimize_time)
    print(output)
    print('Creating the files Route.txt and Routecropped.txt with pixels for the path..')
    create_route_file(path_list,vertex_data)
    print('Done')
    print('Would you like to plot the result from Route.txt into the brandeis map? (Requires the python package PIL to be installed)')
    print('y/n - default n? ')
    plot = input()
    if plot.lower() == 'y':
        plot_on_map()
    
    return


def output_for_samples(vertex_data, edge_data):
    filename = 'sample_output_cases.txt'
    file = open(r"Output.txt","w+") 
    with open(filename) as f:
        for line in f:
            fields = line.split()
            board = fields[3].split('=')[1]
            time = fields[4].split('=')[1]
            if board == 'n':
                has_board = False
            else:
                has_board = True
                
            if time == 'n':
                minimize_time = False
            else:
                minimize_time = True
            start_vertex = get_vertex_id(fields[1],vertex_data)
            end_vertex = get_vertex_id(fields[2],vertex_data)
            path_list, output = find_path(start_vertex, end_vertex, vertex_data, edge_data, has_board, minimize_time)
            
            file.write(line+'\n')
            file.write(output)


            
def tour_outputs_vertex_J(vertex_data, edge_data):
    start_vertex = get_vertex_id('J',vertex_data)
    
    graph_new = construct_graph(vertex_data[5:], edge_data[20:], False, False) #delete the black hole and corners vertices and edges
    min_tree_edges = min_span_tree(graph_new, start_vertex, edge_data[20:])
    file = open(r"OutputP.txt","w+")
    file.write(plotting_cordinates_from_edges(min_tree_edges, edge_data, vertex_data))
    
    krus_edge = kruskal_min_spanning_tree(edge_data[20:], vertex_data[5:], graph_new)
    file = open(r"OutputK.txt","w+")
    file.write(plotting_cordinates_from_edges(krus_edge, edge_data, vertex_data))
    
    file = open(r"OutputPP.txt","w+") 
    file.write(prim_preorder(start_vertex, vertex_data, edge_data))
    
    file = open(r"OutputPS.txt","w+") 
    file.write(prim_shortcut(start_vertex, vertex_data, edge_data))
    
    file = open(r"OutputKP.txt","w+") 
    file.write(kruskal_preorder(start_vertex, vertex_data, edge_data))
    
    return
    

vertex_data = create_vertex_data()
edge_data = create_edge_data()
run_map(vertex_data, edge_data)
#output_for_samples(vertex_data, edge_data)
#tour_outputs_vertex_J(vertex_data, edge_data) #used to create the several output files


