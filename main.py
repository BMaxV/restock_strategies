import matplotlib.pyplot as plt
import random
import math

#ok so for the moment this is simply set up to account for one distribution
#center

#and the distribution center is not billing you for frequency.
#so it's not done

#test


class lager:
    def __init__(self):
        #this is what it costs you to store something
        #this doesn't have to be absolute volume,
        #it can be square meters too, if you have
        #something that simply occupies that space and
        #you can't stack it.
        
        self.cost_per_stored_volume=1 #flat space limiting fee
        self.cost_per_stored_value=1 #opportunity costs, security, etc.
        
        self.cost_per_transport_volume=10  #as a flat fee on the volume
        self.cost_per_transport_value=0.01 #as a fraction of the value of things transported
        #maybe there is a limit on how much people are willing to 
        #transport at once,
        self.maximum_transport_volume=10000
        self.maximum_transport_value=10000
        
        self.flat_transport_fee=200
        self.diversity_fee=2000 #cost per item type you're transporting.
        
        self.maximum_volume_stored=0
        self.maximum_value_stored=0
        
        self.goods=[]
        self.strategies={"fixed volume":self.refill_fixed_volume_check,
                        "minimum volume":self.refill_minimum_volume_check,
                        "minimum volume time":self.refill_minimum_volume_time_check}
        
        self.pick_strategy()
        
        self.chosen_strategy=None
        
        self.time=0
        
    
                
    def order_refill(self,time=1):
        """when the lager restocks, this is the function to do it."""
        if self.time%time==0:
            total_volume=0
            diversity=0
            for g in self.goods:
                if g.needs_refill:
                    total_volume+=g.maximum - g.current
                    g.order_refill()
                    diversity+=1
            if total_volume!=0:
                
                self.sim_volume_cost_track+=self.transport_cost(total_volume,0,diversity)
                self.order_time.append(self.time)
                self.sim_volume_cost.append(self.sim_volume_cost_track*0.01)
                
                self.sim_diversity_cost_track+=diversity*self.diversity_fee
                self.sim_diversity_cost.append(self.sim_diversity_cost_track*0.01)
        #return cost
            
    def max_transport_costs(self):
        c=self.transport_cost(self.maximum_transport_volume,self.maximum_transport_value,1)
        return c
        
    def transport_cost(self,vol,val,div,fee=200,div_fee=10,cptvol=10,cptval=0.01):
        
        #hm the transport costs should probably be affected by the number
        #of things that I move... like the diversity 
        
        flat_fees=math.ceil((vol+1)/self.maximum_transport_volume)*fee
        cost=(vol * cptvol#self.cost_per_transport_volume
             +val * cptval#self.cost_per_transport_value
             +flat_fees)
        return cost
    
    def transport_key_points(self,plot=False):
        volume=[
                self.maximum_transport_volume/4,
                self.maximum_transport_volume/3,
                self.maximum_transport_volume/2,
                self.maximum_transport_volume/1.25,
                self.maximum_transport_volume,
                self.maximum_transport_volume+1,
                self.maximum_transport_volume*2,
                ]
        ps=[]
        pd=[]
        psfee=[]
        pdfee=[]
        psvolprice=[]
        pdvolprice=[]
        for v in volume:
            ps.append(self.transport_cost(v,0,1))
            psfee.append(self.transport_cost(v,0,1,2*self.flat_transport_fee))
            psvolprice.append((self.transport_cost(v,
                                                    0,
                                                    1,
                                                    self.flat_transport_fee,
                                                    self.cost_per_transport_volume*1.025)))
        for v in volume:
            pd.append((self.transport_cost(v,0,1))/(v+1))
            pdfee.append((self.transport_cost(v,0,1,2*self.flat_transport_fee))/(v+1))
            pdvolprice.append((self.transport_cost(v,
                                                0,
                                                1,
                                                self.flat_transport_fee,
                                                self.cost_per_transport_volume*1.025))/(v+1))
        
        if plot:
            plt.plot(volume,pd,label="all default")
            plt.plot(volume,pdfee,label="double fee")
            plt.plot(volume,pdvolprice,label="vol price +25%")
            plt.legend()
            plt.xlabel("volume")
            plt.ylabel("price per volume")
            plt.show()
        
            
        
    
    def storage_cost(self):
        cost=self.cost_per_stored_volume+self.cost_per_stored_value
        return cost
    
    
    
    def refill_fixed_volume_check(self,volume=400):
        """refill if all stockes if the total volume missing
        reaches a certain number"""
        tickneed=0
        for g in self.goods:
            
            tickneed+=g.maximum-g.current
            #loss=consumption*random.random()
            #self.current-=loss
            
        if tickneed > volume:
            for g in self.goods:
                g.needs_refill=True
        
    def refill_minimum_volume_check(self):
        """refill any good when it drops below a minimum volume"""
        for g in self.goods:
            if g.current < g.maximum*g.limit:
                g.needs_refill=True
            
        
    def refill_minimum_volume_time_check(self):
        """refill a good when it is below a minimum volume at a certain
        point in time,usually the point when you check or order new
        stuff"""
        for g in self.goods:
            if g.current < g.maximum*g.limit:
                g.needs_refill=True
    
    def pick_strategy(self):
        a=1
        #ok so there is an optimal strategy for every situation
        
        
    
    def sim(self,plot=False):
        """ simulate the chosen strategy and plot stocks and costs 
        returns list of diversity costs and volume costs,
        which means 
        cost per item (volume like 500kg flour)
        cost per item (as a new different item like flour, sugar, salt)"""
        self.time=0
        tm=100
        #self.sim_volume_cost_track=0
        self.order_time=[0]
        #self.sim_cumulative_cost=[0]
        self.sim_diversity_cost_track=0
        self.sim_diversity_cost=[0]
        self.sim_volume_cost_track=0
        self.sim_volume_cost=[0]
        timeaxis=[]
        while self.time < tm:
            tickneed=0
            
            for g in self.goods:
                loss=g.loss()
                g.current-=loss
                r=g.check_current()
                g.levels.append(g.current)
                #refill
                #for g in self.goods:
                #    g.order_refill()
            self.strategies[self.chosen_strategy]()
            tint=1
            if self.chosen_strategy=="minimum volume time":
                tint=7
            self.order_refill(tint)
            timeaxis.append(self.time)
            self.time+=1
        if plot:
            
            axes = plt.gca()
            axes.set_xlim([-5,105])
            axes.set_ylim([0,500])
            for g in self.goods:
                plt.plot(timeaxis,g.levels,label=g.name)
            plt.plot(self.order_time,self.sim_diversity_cost,label="cost of item diversity")
            plt.plot(self.order_time,self.sim_volume_cost,label="cost of transport")
            plt.title(self.chosen_strategy)
            
            plt.legend()
            print("final costs",self.sim_volume_cost_track)
            print("number of trips",len(self.sim_volume_cost))
            print("cost to diversity",self.sim_diversity_cost_track)
            plt.show()
        
        return self.order_time,self.sim_diversity_cost,self.sim_volume_cost
class good:
    def __init__(self,name="dummy",max_=100,current=0,limit=0.4,consumption=10):
        self.name=name
        self.maximum=max_
        self.current=current
        self.limit=limit
        self.consumption=consumption
        self.levels=[]
        self.needs_refill=False
    
    def check_current(self):
        return self.current < self.limit*self.maximum
            
            #self.order_refill()
    
    def order_refill(self):
        self.current=self.maximum
        self.needs_refill=False
    
    def loss(self):
        loss=random.random()*self.consumption
        return loss
        
def test_all():
    test_transport_costs()
    test_all_strategies()
    
def test_transport_costs(plot=False):
    l=lager()
    a=good(150,0,0.3,15)
    b=good(100,0,0.2,5)
    c=good(500,0,0.005,10)
    l.goods=[a,b,c]
    l. transport_key_points(plot=plot)
    #test_sim()
    a=1

    
def test_all_strategies():
    #ok so the first one *obviously* cuts down the number of trips
    #and a lot more than the other two.
    
    #from the other two, the one with time checks is better,
    #because somewhat obviously, no wait this isn't obvious at all.
    #hm. weird. it reduces the number of trips slightly though.
    
    #this the result if I transport from the same location,
    #If I have to make stops or simply order transport that can't
    #rideshare, this efficiency by bundling should go away
    #or be reduced by loading/unloading/waiting inefficiencies.
    #I THINK...
    
    
    plot=False #plot the individual strategies
    
    x1,vc1,dc1=test_fcv(plot)
    x2,vc2,dc2=test_mvc(plot)
    x3,vc3,dc3=test_mvtc(plot)
    
    plt.plot(x1,vc1,label="fixed volume")
    plt.plot(x2,vc2,label="fixed time")
    plt.plot(x3,vc3,label="minimum volume time")
    plt.legend()
    plt.show()
    
    plt.plot(x1,dc1,label="fixed volume")
    plt.plot(x2,dc2,label="fixed time")
    plt.plot(x3,dc3,label="minimum volume time")
    plt.legend()
    plt.show()
    
def create_dummy_goods(l):
    a=good("a",150,0,0.3,15)
    b=good("b",100,0,0.2,5)
    c=good("c",500,0,0.1,10)
    l.goods=[a,b,c]
    
def test_fcv(plot=False):
    l=lager()
    l.chosen_strategy="fixed volume"
    create_dummy_goods(l)
    
    x,vc,dc = l.sim(plot)
    
    return x,vc,dc 
    
def test_mvc(plot=False):
    l=lager()
    l.chosen_strategy="minimum volume"
    create_dummy_goods(l)
    
    x,vc,dc = l.sim(plot)
    
    return x,vc,dc 
    
def test_mvtc(plot=False):
    l=lager()
    l.chosen_strategy="minimum volume time"
    create_dummy_goods(l)
    
    x,vc,dc = l.sim(plot)
    
    return x,vc,dc 
    



if __name__=="__main__":
    test_all()
