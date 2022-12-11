#!/usr/bin/env python
# coding: utf-8

# #### Importing libraries and reading files

# In[1]:


import pandas as pd
from queue import deque
from collections import namedtuple, defaultdict
from heapq import heappop, heappush


# In[2]:


pages = pd.read_csv('simple_english_wiki_pages.csv')
pages.head()


# In[3]:


pagelinks = pd.read_csv('simple_english_wiki_pagelinks.csv')
pagelinks.head()


# In[6]:


Edge = namedtuple('Edge', 'src dst distance')

class Graph:
    
    def __init__(self):
        self.neighbors = defaultdict(list)
        self.nodes = set()
#         self.viz = graphviz.Digraph('graph')
#         self.viz.attr(rankdir='LR', size='8,5')
        
        
    def add_edge(self, edge: Edge):
        self.neighbors[edge.src].append(edge)
        self.nodes.add(edge.src)
        self.nodes.add(edge.dst)
        
    def __getitem__(self, item):
        return self.neighbors.get(item, [])


# #### Task 1
# Какое наименьшее количество переходов по ссылкам нужно сделать, чтобы прийти от статьи Analytics к статье Algorithm?
# В ответ запишите целое число.

# #### Task 2
# Какая статья на кратчайшем пути из предыдущей задачи (шаг 2) содержит ссылку на статью Algorithm? Напишите название статьи в том же формате, в котором она представлена в датасете.

# In[48]:


start = pages[pages.page_title == 'Analytics'].page_id.values[0]
end = pages[pages.page_title == 'Algorithm'].page_id.values[0]

start, end # id Analytics, id Algorithm


# In[ ]:


# Построение графа (без учета длин ребер)

g_1 = Graph()
for i in range(pagelinks.shape[0]):
    pl_from = pagelinks.iloc[i, 0]
    pl_to = pagelinks.iloc[i, 2]
    g_1.add_edge(Edge(pl_from, pl_to, 1))


# In[9]:


# Поиск(обход) графа в ширину
# V вершины, E - рёбра

def bfs(graph: Graph, start: str):
    
    seen = set()
    v_queue = deque()
    v_queue.append((start, 0))
    result = [(start, 0)]
    while v_queue:
        current, current_level = v_queue.popleft()
        children = [edge.dst for edge in graph[current]]
        for child in children:
            if child not in seen:
                seen.add(child)
                child_level = (child, current_level + 1)
                v_queue.append(child_level)
                child_level_for_result = (current, child, current_level + 1)
                result.append(child_level_for_result)
                
    return result
    


# In[51]:


li_1 = bfs(g_1, start)

for k in li_1:
    if k[1] == end:
        print('Task 1:', k[2])
        print('Task 2:', pages[pages.page_id==k[0]].page_title.values[0])


# #### Task 3
# Задача такая же, как в шаге 2, но теперь мы еще и учитываем длину ссылки. Например:
# 
# Путь Cooking -> Wood(4) -> Building(8) -> Concrete(8) имеет длину 20, а путь Cooking -> Oven(4) -> Brick(5) -> Concrete(8) имеет длину 17.
#  
# 
# Нужно найти кратчайший (по сумме длин всех переходов) путь из аналитики в алгоритмы (Analytics -> Algorithm) :)

# #### Task 4 
# Аналогично заданию 3 - нужно написать название статьи, которая ведет на статью Algorithm в кратчайшем пути из задачи 4.

# In[ ]:


# Построение графа (с учетом длин ребер - алгоритм Дейкстры)

g = Graph()
for i in range(pagelinks.shape[0]):
    pl_from = pagelinks.iloc[i, 0]
    pl_title = pagelinks.iloc[i, 1]
    pl_to = pagelinks.iloc[i, 2]
    g.add_edge(Edge(pl_from, pl_to, len(pl_title)))


# In[43]:


# Поиск кратчайших путей в взвешенном графе (алгоритм Дейкстры)
# V - vertices
# E - edges

def dijkstra(graph: Graph, start):
    heap, seen_vertices, min_distances = [(0, start)], set(), {start: 0}
    result = []
    steps = []
    while heap: # O(V)
        curr_distance, current_vertex = heappop(heap) #O(logV) # start in vertex with min score
        if current_vertex not in seen_vertices:
            
            for _, next_vertex, distance in graph.neighbors.get(current_vertex, []): # O(E)
                if next_vertex in seen_vertices:
                    continue
                    
                prev_min_distance = min_distances.get(next_vertex)
                new_distance = curr_distance + distance
                
                if prev_min_distance is None or new_distance < prev_min_distance:
                    min_distances[next_vertex] = new_distance
                    result.append((current_vertex, next_vertex, new_distance))
                    heappush(heap, (new_distance, next_vertex)) # O(logV)
                    
            seen_vertices.add(current_vertex)

    return result


# O(ElogV + VlogV)


# In[52]:


li = dijkstra(g, start)

for k in li:
    if k[1] == end:
        print('Task 3:', k[2])
        print('Task 4:', pages[pages.page_id==k[0]].page_title.values[0])

