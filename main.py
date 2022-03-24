from bs4 import BeautifulSoup
import requests
import networkx as nx
g=nx.Graph()
def my_neighbours(queue,visited):
    central_node=queue[0]
    n_queue=[]
    while(len(queue)>0):
        try:
            res=requests.get(central_node)
            soup = BeautifulSoup(res.text,"lxml")
            nlink=[]
            print("\n"+str(len(queue)))
            try:
                for link in soup.find_all('a'):
                    temp=link.get('href')
                    if(temp!=""):
                        if(temp.startswith("http://www.iitrpr.ac.in")):
                            nlink.append(temp)
                        elif(temp.startswith("/")):
                            nlink.append("http://www.iitrpr.ac.in"+temp)
                        elif(not(temp.startswith("http")) and not(temp.startswith("/"))):
                            nlink.append("http://www.iitrpr.ac.in/"+temp)
                for link in nlink:
                    if(link not in visited):
                        visited.append(link)
                        n_queue.append(link)
                    g.add_edge(central_node, link)
            except AttributeError:
                central_node=queue[0]
                del queue[0]
            else:
                central_node=queue[0]
                del queue[0]
        except(requests.exceptions.MissingSchema, requests.exceptions.ConnectionError, requests.exceptions.InvalidURL,requests.exceptions.InvalidSchema):
            continue
    return n_queue,visited
central_node="http://www.iitrpr.ac.in"
visited=[central_node]
res=requests.get(central_node)
soup = BeautifulSoup(res.text,"lxml")
nlink=[]
for link in soup.find_all('a'):
    temp=link.get('href')
    if(temp!=""):
        if(temp.startswith("http://www.iitrpr.ac.in")):
            nlink.append(temp)
        elif(temp.startswith("/")):
           nlink.append("http://www.iitrpr.ac.in"+temp)
        elif(not(temp.startswith("http")) and not(temp.startswith("/"))):
           nlink.append("http://www.iitrpr.ac.in/"+temp)
#first neighbours
queue1=nlink[:]
for link in nlink:
    visited.append(link)
    g.add_edge(central_node, link)
#second neighbours
queue2,visited=my_neighbours(queue1,visited)
#third neighbours
queue3,visited=my_neighbours(queue2,visited)
nx.draw(g)