import networkx as nx;
import community
import datetime 
begin = datetime.datetime.now();
G = nx.Graph()
G.add_edge('a','b'); G.add_edge('b','a');
G.add_edge('b','f'); G.add_edge('f','b');
G.add_edge('a','d'); G.add_edge('d','a');
G.add_edge('d','f'); G.add_edge('f','d');
G.add_edge('a','f'); G.add_edge('f','a');
G.add_edge('f','g'); G.add_edge('g','f');
G.add_edge('g','h'); G.add_edge('h','g');
G.add_edge('g','j'); G.add_edge('j','g');

#edges = nx.edge_betweenness_centrality(G);
par = community.best_partition(G);

end = datetime.datetime.now();
print((end-begin));

print(par);
#print(edges);