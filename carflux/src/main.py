import numpy as np
import simpy
import networkx as nx
import datetime
import folium
from folium import plugins
from agent import Agent
from world import World
import pickle as pkl

class Traveller(Agent):
    
    def __init__(self,id_,origin,dest,color='red'):
        self.id_ = id_
        self.origin = origin
        self.dest = dest
        self.path_ = nx.shortest_path(CityGraph,origin,dest)
        #self.current_node = origin
        self.current_index = 0
        self.next_index = 1
        self.entered_edge = 0
        self.dest_reached = False
        self.map_lines = []
        self.color = color
        self.transit_time = (CityGraph.get_edge_data(self.path_[self.current_index],self.path_[self.next_index])[0]['travel_time'])
        self.current_time = datetime.datetime.fromisoformat('2021-09-17T00:00:01')
        
    def communicate(self):
        tick = env.now
        _current_node, _next_node = self.path_[self.current_index],self.path_[self.next_index]
        with open('res-graph-walk.csv','a') as fh:
            fh.write('%s,%s,%s,%s\n'%(self.id_,tick,self.path_[self.current_index],self.path_[self.next_index]))

    def perceive(self):
        pass
    
    def react(self):
        pass
        
        
            
    def update_state(self):
        # fetch path info
        self.current_time = self.current_time + datetime.timedelta(seconds=1)
        if self.current_index < len(self.path_)-1:
            tick = env.now
            ##self.next_index = self.current_index + 1
            print(self.next_index)
            
            #self.transit_time = (CityGraph.get_edge_data(self.path_[self.current_index],self.path_[self.next_index])[0]['travel_time'])
            if (tick - self.entered_edge)>= self.transit_time:
                self.next_index = self.current_index + 1
                self.transit_time = (CityGraph.get_edge_data(self.path_[self.current_index],self.path_[self.next_index])[0]['travel_time'])
                _current_node, _next_node = self.path_[self.current_index],self.path_[self.next_index]
                self.map_lines.append({"coordinates":[
                                    [CityGraph.nodes[_current_node]['x'],CityGraph.nodes[_current_node]['y']],
                                    [CityGraph.nodes[_next_node]['x'],CityGraph.nodes[_next_node]['y']]
                                    ],
                                    "dates":[datetime.datetime.isoformat(self.current_time),datetime.datetime.isoformat(self.current_time+ datetime.timedelta(seconds=self.transit_time))],
                                    "color":self.color,
                                    "weight": 15},)
                self.current_index = self.next_index
                self.entered_edge = tick

    def react(self):
        pass
        #self.current_time = self.current_time + datetime.timedelta(seconds=1)
        #if self.current_index < len(self.path_)-1:
        #    self.update_state()
        #    self.communicate()




def simulate_agents():
    global CityGraph
    CityGraph = nx.read_gpickle('../data/london.gpickle')
    nodes_data = list(CityGraph.nodes.data())
    t = Traveller(id_=1,origin=nodes_data[2][0],dest=nodes_data[18][0])
    t1 = Traveller(id_=2,origin=nodes_data[3][0],dest=nodes_data[15][0],color='green') 
    city_grid = World(list_agents=[t,t1],list_resources=[])
    
    global env
    env = simpy.Environment()
    #tick = env.now
    env.process(city_grid.simulate_time_step(env))
    env.run(until=200)
    dump_visualization_files([t,t1])


def dump_visualization_files(list_traveller_obj):
    with open('trajectories.pkl','wb') as fh:
        pkl.dump(list_traveller_obj,fh)

def generate_trajectory_map():
    with open('trajectories.pkl','rb') as fh:
        list_traveller_obj = pkl.load(fh)
    trajectories = [t.map_lines for t in list_traveller_obj]
    print(trajectories)
    m = folium.Map(location=[51.5,0.12],zoom_start=1000)#location=[51.499055, 0.1139217],zoom_start=5)

    features = [
        {
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": line["coordinates"],
            },
            "properties": {
                "times": line["dates"],
                "style": {
                    "color": line["color"],
                    "weight": line["weight"] if "weight" in line else 5,
                },
            },
        }
        for line in trajectories[0]+trajectories[1]
    ]

    plugins.TimestampedGeoJson(
        {
            "type": "FeatureCollection",
            "features": features,
        },
        period="PT1S",
        add_last_point=True,
    ).add_to(m)
    m.save("trajectories.html")




if __name__ == "__main__":
    simulate_agents()
    generate_trajectory_map()





    
            


