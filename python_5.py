from random import randrange as rand


class Engine():

    def __init__(self, fuel='gasoline', consumption=0.08):
        self.consumption = consumption


class Fuel():

    def __init__(self, fuel='gasoline', cost=2.4):
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
        if fuel == 'gasoline':
            if keyword == 'car':
                self.value = cost
            elif keyword == 'fuel':
                self.value = 2.4
            elif keyword == 'loss':
                self.value = 9.5
            elif keyword == 'serv':
                self.value = 500
        elif fuel == 'diesel':
            if keyword == 'car':
                self.value = cost
            elif keyword == 'fuel':
                self.value = 1.8
            elif keyword == 'loss':
                self.value = 10.5
            elif keyword == 'serv':
                self.value = 700
        else:
            self.value = cost


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
        self.count = 0

    def run(self, car):
        car.cost -= car.service.cost
        self.count += 1


class Car(object):
    __total_cars = []

    def __init__(self, name='Noname'):
        self.__total_cars.append(name)
        self.number = len(self.__total_cars)
        self.name = name
        self.__tahograph = 0
        self.__utilize = False
        self.tank = self.choose_tank()
        self.engine = self.choose_engine()
        self.cost = Cost().value
        self.service = Service(self.tank.fuel)
        self.route = Way('route', rand(55000, 286000))
        self.remain_mileage = 0

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
            return Engine('diesel', 0.06)

    @property
    def tahograph(self):
        return self.__tahograph

    @tahograph.setter
    def tahograph(self, value):
        pass

    def run(self, way_gone=0):
        thousands_of_kilometers = 0
        while way_gone <= self.route.length and not self.__utilize:
            if self.cost <= 0:
                self.__utilize = True
            else:
                raise_rate = 1.01 ** (way_gone // 1000)
                way_gone += self.tank.capasity / \
                    (self.engine.consumption * raise_rate)
                if way_gone // 1000 > thousands_of_kilometers:
                    self.cost -= Cost('loss', self.tank.fuel.type).value
                    thousands_of_kilometers += 1
                if (way_gone // Way(self.fuel.type).length)\
                        > self.service.count:
                    self.service.run(self)
                else:
                    self.tank.fuel_up()
        if self.__utilize:
            self.__tahograph += way_gone
            self.cost = 0
        else:
            self.__tahograph += self.route.length

    def run_till_util(self):
        saved_tahograph = self.__tahograph
        saved_cost = self.cost
        saved_fuel_up_cost = self.tank.fuel_up_cost
        saved_fuel_up_count = self.tank.fuel_up_count
        saved_service_count = self.service.count
        while not self.__utilize:
            self.run()
        self.remain_mileage = int(self.tahograph - saved_tahograph)
        self.__tahograph = saved_tahograph
        self.cost = saved_cost
        self.tank.fuel_up_cost = saved_fuel_up_cost
        self.tank.fuel_up_count = saved_fuel_up_count
        self.service.count = saved_service_count


cars = [Car() for _ in range(100)]
for car in cars:
    car.run()
    car.run_till_util()
cars_diesel = list(filter(lambda car: car.tank.fuel.type == 'diesel', cars))
cars_diesel.sort(key=lambda car: car.cost, reverse=True)
cars_gasoline = list(filter(lambda car: car.tank.fuel.type == 'gasoline', cars))
cars_gasoline.sort(key=lambda car: car.remain_mileage, reverse=True)
print('Diesel cars, by remain cost:')
for car in cars_diesel:
    print('Car #{}, {}, cost: {}'.format(car.number, car.name, car.cost))
print('\nGasoline cars, by remain mileage:')
for car in cars_gasoline:
    print('Car #{}, {}, milege: {}'.format(car.number, car.name, car.remain_mileage))
print('\nTotal cars remain cost:\n\t', sum([car.cost for car in cars]))
