from multiprocessing.pool import ThreadPool
from threading import Lock

class World:

    # Probably a bit risque.
    def __init__(self,list_agents,list_resources):
        self.agents = list_agents
        self.shared_resources = list_resources
    
    # Getter methods
    def get_agents(self):
        return self.agents
    
    def get_resources(self):
        return self.shared_resources
        
    
    def simulate_time_step(self,env):
        #global simulate_agent
        def simulate_agent(agent):
            agent.perceive()
            with Lock():
                agent.update_state()
                agent.react()
            agent.communicate()
            #return 1
            
            
        while True:
            with ThreadPool(processes=8) as tp:
                res = tp.map(simulate_agent,self.get_agents())
            print('one time step')
            #for shared_resource in self.get_resources():
            #    shared_resource.update()
            yield env.timeout(1)