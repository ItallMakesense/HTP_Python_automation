from random import randrange as rand
import sys
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.addHandler(logging.FileHandler("car_report.log"))


class Engine():

    def __init__(self, consumption=0.08):
        self.consumption = consumption
        self.cons_increase_rate = 1.01
        self.cons_increase_point = 1000


class Fuel():

    def __init__(self, fuel='gasoline', cost=2.2):
        self.type = fuel
        self.cost = Cost('fuel', self.type, cost).value


class Tank():

    def __init__(self, fuel, capasity=60):
        self.fuel = fuel
        self.capasity = capasity
        self.fuel_up_count = 0
        self.fuel_up_cost = 0

    def fuel_up(self):
        self.fuel_up_cost += self.capasity * self.fuel.cost
        self.fuel_up_count += 1


class Cost():

    def __init__(self, keyword='car', fuel='gasoline', cost=10000):
        self.value = cost
        if fuel == 'gasoline':
            if keyword == 'car':
                self.loss = 9.5
            elif keyword == 'serv':
                self.value = 500
        elif fuel == 'diesel':
            if keyword == 'car':
                self.loss = 10.5
            elif keyword == 'serv':
                self.value = 700


class Way():

    def __init__(self, fuel=None, length=42):
        if fuel == 'gasoline':
            self.length = 100000
        elif fuel == 'diesel':
            self.length = 150000
        else:
            self.length = length


class Service():

    def __init__(self, fuel, other_cost=False):
        if other_cost:
            self.cost = other_cost
        else:
            self.cost = Cost('serv', fuel.type).value
            self.point = Way(fuel.type).length
        self.count = 0

    def run(self, given_car):
        given_car.cost.value -= self.cost
        self.count += 1


class Car(object):
    __total_cars = []

    def __init__(self, name='Noname'):
        self.__total_cars.append(name)
        self.number = len(self.__total_cars)
        self.name = name
        self.__tahograph = 0
        self.tank = self.choose_tank()
        self.engine = self.choose_engine()
        self.cost = Cost()
        self.service = Service(self.tank.fuel)
        self.route = Way('route', rand(55000, 286000)).length
        self.remain_mileage = 0
        self.engine_utilized = False
        self.possible_credit = 0

    @property
    def fuel(self):
        if not self.number % 3:
            return Fuel('diesel', 1.8)
        else:
            return Fuel()

    def choose_tank(self):
        if not self.number % 5:
            return Tank(self.fuel, 75)
        else:
            return Tank(self.fuel)

    def choose_engine(self):
        if self.tank.fuel.type == 'gasoline':
            return Engine()
        elif self.tank.fuel.type == 'diesel':
            return Engine(0.06)

    @property
    def tahograph(self):
        return self.__tahograph

    @tahograph.setter
    def tahograph(self, value):
        pass

    def run(self, way_gone=0):
        thousands_of_kilometers = 0
        consumption_at_moment = self.engine.consumption
        while way_gone <= self.route:
            if self.tank.capasity / 10 <= consumption_at_moment:
                self.engine_utilized = True
                self.engine = self.choose_engine()
                self.cost.value -= 3000
                if self.__tahograph < self.route:
                    continue
                else:
                    break
            else:
                way_gone += self.tank.capasity / consumption_at_moment
            if way_gone // self.engine.cons_increase_point > \
               thousands_of_kilometers:
                self.cost.value -= self.cost.loss
                consumption_at_moment *= self.engine.cons_increase_rate
                thousands_of_kilometers += 1
            if (way_gone // self.service.point) > self.service.count:
                self.service.run(self)
            else:
                if way_gone > 50000 and self.tank.fuel.cost == 2.2:
                    self.tank.fuel = Fuel('gasoline', 2.4)
                else:
                    self.tank.fuel_up()
        if self.engine_utilized:
            self.__tahograph += way_gone
            self.engine_utilized = False
        else:
            self.__tahograph += self.route
        self.engine.consumption = consumption_at_moment

    def run_till_util(self):
        saved_tahograph = self.__tahograph
        saved_consumption = self.engine.consumption
        saved_cost = self.cost.value
        saved_fuel_up_cost = self.tank.fuel_up_cost
        saved_fuel_up_count = self.tank.fuel_up_count
        saved_service_count = self.service.count
        while self.cost.value > 0:
            self.run()
        self.possible_credit = abs(self.cost.value)
        self.remain_mileage = int(self.tahograph - saved_tahograph)
        self.__tahograph = saved_tahograph
        self.engine.consumption = saved_consumption
        self.cost.value = saved_cost
        self.tank.fuel_up_cost = saved_fuel_up_cost
        self.tank.fuel_up_count = saved_fuel_up_count
        self.service.count = saved_service_count


cars = [Car() for _ in range(100)]
for car in cars:
    car.run()
    car.run_till_util()
    logger.info('Car #{} ({}) Mileage: {}'.format(
        car.number, car.name, car.tahograph))
cars_diesel = list(filter(lambda car: car.tank.fuel.type == 'diesel', cars))
cars_diesel.sort(key=lambda car: car.cost.value, reverse=True)
cars_gasoline = list(
    filter(lambda car: car.tank.fuel.type == 'gasoline', cars))
cars_gasoline.sort(key=lambda car: car.remain_mileage, reverse=True)
print('\nTotal cars remain cost:\n\t', sum([car.cost.value for car in cars]))
print('\nTotal cars possible credit:\n\t',
      sum([car.possible_credit for car in cars]))
