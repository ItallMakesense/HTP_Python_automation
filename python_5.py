import random
import pprint


class Car(object):
    _object_count = []
    _tahograph = 0
    petrol = 2.4
    diesel = 1.8
    overhaul = False
    _utilize = False

    def __init__(self, name='Noname'):
        self._object_count.append(len(self._object_count) + 1)
        if len(self._object_count) % 3 == 0:
            self.fuel_type = self.diesel
            self.max_run = 150000
            self.liter_run = 6 / 100
            self.service = 700
            self.way_cost_lowering = 10.5
        else:
            self.fuel_type = self.petrol
            self.max_run = 100000
            self.liter_run = 8 / 100
            self.service = 500
            self.way_cost_lowering = 9.5
        if len(self._object_count) % 5 == 0:
            self.tank = 75
        else:
            self.tank = 60
        self.cost = 10000
        self.service_cost = 0
        self.service_done = 0
        self.fuel_cost = 0
        self.fuel_ups = 0
        self.mileage = 0
        self.mileage_before_util = 0
        self.run()

    def take_to_service(self):
        self._tahograph = self.mileage
        if self.cost > self.service:
            self.service_cost += self.service
            self.service_done += 1
            self.overhaul = False
        else:
            self._utilize = True

    def fuel_up(self):
        self.fuel_cost += self.tank * self.fuel_type
        self.fuel_ups += 1

    def run(self, way=random.randrange(55000, 286000)):
        while self.mileage != way:
            if self._utilize:
                print ("Well, it's done.")
                break
            if self.overhaul:
                self.take_to_service()
            self.mileage += 1
            if self.mileage % 1000 == 0:
                self.cost -= self.way_cost_lowering
                self.liter_run *= 1.01
            if self.mileage % (self.tank / self.liter_run) == 0:
                self.fuel_up()
            if self.mileage % self.max_run == 0:
                self.overhaul = True

car = Car()
print(len(car._object_count), car.mileage, car.cost, car.fuel_cost, car.fuel_ups)
