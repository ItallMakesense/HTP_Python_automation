from random import randrange as rand


class Engine():

    def __init__(self, fuel='gasoline', consumption=0.08):
        self.consumption = consumption


class Fuel():

    def __init__(self, fuel='gasoline', cost=2.4):
        self.type = fuel
        self.cost = Cost('fuel', self.type, cost)


class Tank():

    def __init__(self, capasity=60):
        self.capasity = capasity


class Cost():

    def __init__(self, keyword='car', fuel='gasoline', cost=10000):
        if fuel == 'gasoline':
            if keyword == 'fuel':
                self.value = 2.4
            elif keyword == 'cost_down':
                self.value = 9.5
            elif keyword == 'service':
                self.value = 500
            elif keyword == 'car':
                self.value = cost
        elif fuel == 'diesel':
            if keyword == 'fuel':
                self.value = 1.8
            elif keyword == 'cost_down':
                self.value = 10.5
            elif keyword == 'service':
                self.value = 700
            elif keyword == 'car':
                self.value = cost
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

    def __init__(self, fuel, cost=False):
        if cost:
            self.cost = cost
        else:
            self.cost = Cost('service', fuel)
        self.count = 0

    def run(self, car):
        car.cost.value -= car.service.cost.value
        self.count += 1


class Car(object):
    __total_cars = []

    def __init__(self, name='Noname', *args):
        self.__total_cars.append(name)
        self.number = len(self.__total_cars)
        self.name = name
        self.__tahograph = 0
        self.__utilize = False
        self.cost = Cost()
        self.service = Service(self.fuel.type)
        self.fuel_ups_cost = 0
        self.fuel_ups_count = 0
        self.route = Way('route', rand(55000, 286000))
        self.remain_mileage = 0

    @property
    def fuel(self):
        if not len(self.__total_cars) % 3:
            return Fuel('diesel', 1.8)
        else:
            return Fuel()

    @property
    def tank(self):
        if not len(self.__total_cars) % 5:
            return Tank(75)
        else:
            return Tank()

    @property
    def engine(self):
        if self.fuel.type == 'gasoline':
            return Engine()
        elif self.fuel.type == 'diesel':
            return Engine('diesel', 0.06)

    @property
    def tahograph(self):
        return self.__tahograph

    @tahograph.setter
    def tahograph(self, value):
        pass

    @property
    def fuel_up(self):
        self.fuel_ups_cost += self.tank.capasity * self.fuel.cost.value
        self.fuel_ups_count += 1

    def run(self, way_gone=0):
        thousands = 0
        while way_gone <= self.route.length and not self.__utilize:
            if self.cost.value <= 0:
                self.__utilize = True
            else:
                raise_rate = 1.01 ** (way_gone // 1000)
                way_gone += self.tank.capasity / \
                    (self.engine.consumption * raise_rate)
                if way_gone // 1000 > thousands:
                    self.cost.value -= Cost('cost_down', self.fuel.type).value
                    thousands += 1
                if (way_gone // Way(self.fuel.type).length)\
                        > self.service.count:
                    self.service.run(self)
                else:
                    self.fuel_up
        if self.__utilize:
            self.__tahograph += way_gone
            self.cost.value = 0
        else:
            self.__tahograph += self.route.length

    def run_till_util(self):
        saved_tahograph = self.__tahograph
        saved_cost = self.cost.value
        saved_fuel_ups_cost = self.fuel_ups_cost
        saved_fuel_ups_count = self.fuel_ups_count
        saved_service_count = self.service.count
        while not self.__utilize:
            self.run()
        self.remain_mileage = self.tahograph - saved_tahograph
        self.__tahograph = saved_tahograph
        self.cost.value = saved_cost
        self.fuel_ups_cost = saved_fuel_ups_cost
        self.fuel_ups_count = saved_fuel_ups_count
        self.service.count = saved_service_count


def cars_type(obj):
    pass


cars = [Car() for _ in range(10)]
for car in cars:
    car.run()
    car.run_till_util()
    print('cost: %s\t gone: %s\t fuel: %s\t fuel count: %s\t remain: %s\n' %
          (int(car.cost.value), car.tahograph, int(car.fuel_ups_cost),
           car.fuel_ups_count, car.remain_mileage))
print('sum:', sum([car.cost.value for car in cars]))
# cars = filter(lambda cost: ) d_car in [filter(lambda : car.fuel.type == 'diesel', car) for car in cars]
