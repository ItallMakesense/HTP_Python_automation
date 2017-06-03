"""
---Car Park---
Здесь представлен класс который, производит легковые автомобили.

Из ста обектов этого класса (машин) создается автопарк машин, где:
- Стоимость литра бензина 2,4$, дизеля – 1,8$.
- Каждый третий автомобиль дизельный (остальные, соответственно, бензиновые)
- Стандартный бензобак 60 литров, а каждый пятый авто – с баком на 75 литров.
- Стоимость каждой машины 10000$.
- Каждая машина имеет тахограф (он считает пройденный километраж),
  который нельзя сбрасывать/уменьшать.
- Максимальный пробег до капремонта бензиновой – 100.000 километров,
  дизельной – 150.000 км.
- Поддерживается капремонт: при подходе срока машина отзывается в СТО
  и проведится капремонт. Его стоимость для бензиновой машины 500$,
  для дизельной – 700$.
- Расход топлива у бензиновой – 8 л/100 км, расход дизеля – 6 л/100 км.
- Каждая 1.000 км пробега снижает стоимость бензиновой машины на 9.5$,
  дизельной – на 10.5$, при этом увеличивая расход топлива на 1%.
- для каждой машины создаётся уникальный маршрут случайной длины (от 55000 до 286000 км),
- Бак авто заправляется каждый раз, как он опустеет.

Машины предоставляют следующие сведения о себе:
- пробег
- остаточная стоимость
- сколько было потрачено на топливо за всю поездку
- сколько раз машина заправлялась
- сколько осталось пробега до утилизации

После пробега все машины в автопарке отсортированы: дизельные – по остаточной стоимости,
бензиновые – по тому сколько им осталось ездить.

Также подсчитана суммарная стоимость машин в автопарке после пробега.
"""

from random import randrange as rand
import threading


class Engine():

    def __init__(self, consumption=0.08):
        self.consumption = consumption
        self.cons_increase_rate = 1.01
        self.cons_increase_point = 1000


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


class Car(threading.Thread):
    __total_cars = []

    def __init__(self, name='Noname'):
        threading.Thread.__init__(self)
        self.__total_cars.append(name)
        self.number = len(self.__total_cars)
        self.name = name
        self.__tahograph = 0
        self.__utilize = False
        self.tank = self.choose_tank()
        self.engine = self.choose_engine()
        self.cost = Cost()
        self.service = Service(self.tank.fuel)
        self.route = Way('route', rand(55000, 286000)).length
        self.remain_mileage = 0

    def run(self):
        self.go()
        self.run_till_util()

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

    def go(self, way_gone=0):
        thousands_of_kilometers = 0
        consumption_at_moment = self.engine.consumption
        while way_gone <= self.route and not self.__utilize:
            if self.cost.value <= 0:
                self.__utilize = True
                self.cost.value = 0
            else:
                if self.tank.capasity / 10 > consumption_at_moment:
                    way_gone += self.tank.capasity / consumption_at_moment
                else:
                    self.__utilize = True
                    continue
                if way_gone // self.engine.cons_increase_point > thousands_of_kilometers:
                    self.cost.value -= self.cost.loss
                    consumption_at_moment *= self.engine.cons_increase_rate
                    thousands_of_kilometers += 1
                if (way_gone // self.service.point) > self.service.count:
                    self.service.run(self)
                else:
                    self.tank.fuel_up()
        if self.__utilize:
            self.__tahograph += way_gone
        else:
            self.__tahograph += self.route
        self.engine.consumption = consumption_at_moment

    def run_till_util(self):
        saved_tahograph = self.tahograph
        saved_consumption = self.engine.consumption
        saved_cost = self.cost.value
        saved_fuel_up_cost = self.tank.fuel_up_cost
        saved_fuel_up_count = self.tank.fuel_up_count
        saved_service_count = self.service.count
        while not self.__utilize:
            self.go()
        self.remain_mileage = int(self.tahograph - saved_tahograph)
        self.__tahograph = saved_tahograph
        self.engine.consumption = saved_consumption
        self.cost.value = saved_cost
        self.tank.fuel_up_cost = saved_fuel_up_cost
        self.tank.fuel_up_count = saved_fuel_up_count
        self.service.count = saved_service_count


cars = [Car() for _ in range(100)]
for car in cars:
    car.start()
    while car.is_alive():
        pass
cars_diesel = list(filter(lambda car: car.tank.fuel.type == 'diesel', cars))
cars_diesel.sort(key=lambda car: car.cost.value, reverse=True)
cars_gasoline = list(filter(lambda car: car.tank.fuel.type == 'gasoline', cars))
cars_gasoline.sort(key=lambda car: car.remain_mileage, reverse=True)
print('Diesel cars, by remain cost:')
for car in cars_diesel:
    print('Car #{}, {}, cost: {}'.format(car.number, car.name, car.cost.value))
print('\nGasoline cars, by remain mileage:')
for car in cars_gasoline:
    print('Car #{}, {}, milege: {}'.format(car.number, car.name, car.remain_mileage))
print('\nTotal cars remain cost:\n\t', sum([car.cost.value for car in cars]))
