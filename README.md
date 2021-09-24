# carflux

1. Create a data folder 
2. Run the following code snippet
<code>
  
G = osmnx.graph_from_place("London")
  
G = osmnx.speed.add_edge_speeds(G)
  
G = osmnx.speed.add_edge_travel_times(G)

nx.write_gpickle(G,'data/london.gpickle')
  
</code>
3. Change to src and run main.py
