import random


class Engine(object):
    __total_engines = []

    def __init__(self, fuel, consumption=0):
        if fuel == 'gasoline':
            self.cons = 0.08
        elif fuel == 'diesel':
            self.cons = 0.06
        else:
            self.cons = consumption


class Fuel(object):

    def __init__(self, fuel_type='gasoline', fuel_cost=2.4):
        self.fuel_type = fuel_type

    @property
    def __call__(self):
        return self.fuel_type

    @property
    def cost(self):
        return Cost('fuel', fuel_cost)


class Tank(object):

    def __init__(self, number):
        if not number % 5:
            self.capasity = 75
        else:
            self.capasity = 60

    @property
    def __call__(self):
        return self.capasity


class Cost(object):

    def __init__(self, dependency="", cost=10000):
        if dependency == 'gasoline':
            self.cost = 9.5
        elif dependency == 'diesel':
            self.cost = 10.5
        else:
            self.cost = cost

    @property
    def __call__(self):
        return self.cost


class Way(object):

    def __init__(self, dependency=None, way=0):
        if dependency == 'gasoline':
            self.way = 100000
        elif dependency == 'diesel':
            self.way = 150000
        else:
            self.way = way
        return self.way

    @property
    def __call__(self):
        return self.way


class Service(object):

    def __init__(self, fuel, cost=0):
        if fuel == 'gasoline':
            self.cost = Cost('service', 500)
        elif fuel == 'diesel':
            self.cost = Cost('service', 700)
        else:
            self.cost = cost

    @property
    def __call__(self):
        return self.cost

    def run(self, car):
        car.cost += self.cost
        self.count += 1


class Tahograph(object):

    def __init__(self):
        self.indication = 0
        return self.indication

    @property
    def __call__(self):
        return self.indication


class Car(object):
    __total_cars = []
    __tahograph = Tahograph()
    __utilize = False

    def __init__(self, name='Noname', *args):
        self.__total_cars.append(name)
        self.name = name
        self.number = len(self.__total_cars)
        self.cost = Cost()
        if not self.number % 3:
            self.fuel = Fuel('diesel', 1.8)
        else:
            self.fuel = Fuel()
        self.service = Service(self.fuel)
        self.fuel_ups_cost = 0
        self.fuel_ups_count = 0

    @property
    def tahograph(self):
        return self.__tahograph

    @tahograph.setter
    def tahograph(self, value):
        pass

    def __call__(self, way=0):
        self.run(way)

    def fuel_up(self):
        self.fuel_ups_cost += Tank(self.number) * self.fuel.cost
        self.fuel_ups_count += 1

    def run(self, way, way_gone=__tahograph):
        while way_gone <= way:
            if self.cost <= 0:
                print("Well, it's done.")
                self.__utilize = True
                break
            else:
                raise_rate = 1.01 ** (way_gone // 1000)
                way_gone += Tank(self.number) / \
                    (Engine(self.fuel).cons * raise_rate)
                if (way_gone // Way(self.fuel)) > self.service.count:
                    self.service.run(self)
                else:
                    self.fuel_up()
        if self.__utilize:
            self.__tahograph = way_gone
            self.cost = 0
        else:
            self.__tahograph = way
            self.cost -= Cost(self.fuel) * self.__tahograph / 1000

car_park = []
for num in range(100):
    car = Car(str(num + 1))
    car_park.append(car)
for car in car_park:
    car(Way(random.randrange(55000, 286000)))
for car in car_park:
    print('cost: {}\n\t mileage: {}\n\t\t fuel cost: {}\n\t\t\t fuel count: {}'.format
          (car.cost, car.tahograph, car.fuel_ups_cost, car.fuel_ups_count))
