class Garaz():

    def __init__(self, space=10) -> None:
        self.cars = []
        self.amountOfSpace = space

    def parking_car(self, color='Black'):
        samochod = Car(color)
        self.cars.append(samochod)
        self.amountOfSpace -= 1

    def __getitem__(self, key):
        return self.cars[key]


class Car():
    def __init__(self, color='Black') -> None:
        self.color = color
        pass

    def __str__(self) -> str:
        return f'Kolor twojego samochodu to {self.color}'


garaz = Garaz()

garaz.parking_car('Red')
garaz.parking_car()

print(garaz[0])
print(garaz[1])
