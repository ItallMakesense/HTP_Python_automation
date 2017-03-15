import random

class Car(object):
    __object_count = []
    __tahograph = 0
    petrol = {'type': 'petrol', 'cost': 2.4}
    diesel = {'type': 'diesel', 'cost': 1.8}
    need_overhaul = False
    __utilize = False

    def __init__(self, name='Noname'):
        self.__object_count.append(name)
        self.name = name
        if (len(self.__object_count) % 3) == 0:
            self.fuel_type = self.diesel['type']
            self.fuel_cost = self.diesel['cost']
            self.max_run = 150000
            self.liter_run = 6 / 100
            self.service = 700
            self.cost_lowering = 10.5
        else:
            self.fuel_type = self.petrol['type']
            self.fuel_cost = self.petrol['cost']
            self.max_run = 100000
            self.liter_run = 8 / 100
            self.service = 500
            self.cost_lowering = 9.5
        if (len(self.__object_count) % 5) == 0:
            self.tank = 75
        else:
            self.tank = 60
        self.cost = 10000
        self.service_cost = 0
        self.service_done = 0
        self.fuel_ups_cost = 0
        self.fuel_ups_count = 0
        self.mileage = 0
        self.mileage_before_util = 0
        
    def __call__(self, way=0):
        self.run(way)
        self.run_till_the_end()
        
    def take_to_service(self):
        self.service_cost += self.service
        self.service_done += 1
        self.need_overhaul = False
        
    def fuel_up(self):
        self.fuel_ups_cost += self.tank * self.fuel_cost
        self.fuel_ups_count += 1

    def run(self, way):
        mileage = 0
        while mileage <= way:
            if self.cost == 0:
                print ("Well, it's done.")
                self.__utilize = True
                break
            else:
                if self.need_overhaul:
                    self.take_to_service()
                else:
                    if (mileage // self.max_run) > self.service_done:
                        self.need_overhaul = True
                        continue
                    raise_rate = 1.01 ** (mileage // 1000)
                    self.fuel_up()
                    mileage += self.tank / (self.liter_run * raise_rate)
        if self.__utilize:
            self.mileage = mileage
            self.cost = 0
        else:
            self.mileage = way
            self.cost -= self.cost_lowering * self.mileage / 1000
        self.__tahograph = self.mileage
        
    def run_till_the_end(self):
        pass
                

car_park = []                
for num in range(100):
    car = Car(str(num + 1))
    car_park.append(car)
for car in car_park:
    car(random.randrange(55000, 286000))
for car in car_park:
    print ('cost: {}\n\t mileage: {}\n\t\t fuel cost: {}\n\t\t\t fuel count: {}'.format\
          (car.cost, car.mileage, car.fuel_ups_cost, car.fuel_ups_count))
    print (car.fuel_type)v
