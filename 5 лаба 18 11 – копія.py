from enum import Enum
from datetime import datetime, timedelta
import math


class Brand(Enum):
    TOYOTA = "Toyota"
    BMW = "BMW"
    AUDI = "Audi"
    MERCEDES = "Mercedes"
    HONDA = "Honda"
    SKODA = "Skoda"


class Car:
    def __init__(self, brand, age, max_speed, horse_power, plate):
        self._brand = brand
        self._age = age
        self._max_speed = max_speed
        self._horse_power = horse_power
        self._plate = plate

    @property
    def brand(self):
        return self._brand

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        if value < 0:
            raise ValueError("Age cannot be negative")
        self._age = value

    @property
    def max_speed(self):
        return self._max_speed

    @property
    def horse_power(self):
        return self._horse_power

    @property
    def plate(self):
        return self._plate

    def show_info(self):
        print(f"{self._brand.value} [{self._plate}] | age: {self._age} y. | "
              f"max speed: {self._max_speed} km/h | "
              f"power: {self._horse_power} hp")

    def __str__(self):
        return f"{self._brand.value} [{self._plate}]"

    def __del__(self):
        print(f"Car {self._brand.value} [{self._plate}] deleted")


class Parking:
    def __init__(self, max_places, price_per_hour):
        self._max_places = max_places
        self._price_per_hour = price_per_hour
        self._cars = []  # records: {"car": Car, "entry": datetime}

    def __del__(self):
        print("Parking closed")

    @property
    def max_places(self):
        return self._max_places

    @property
    def price_per_hour(self):
        return self._price_per_hour

    @price_per_hour.setter
    def price_per_hour(self, value):
        if value <= 0:
            raise ValueError("Price must be positive")
        self._price_per_hour = value

    @property
    def free_places(self):
        return self._max_places - len(self._cars)

    def park_car(self, car, entry_time=None):
        if self.free_places == 0:
            print(f"Parking is full! Cannot park {car}.")
            return False
        entry_time = entry_time or datetime.now()
        self._cars.append({"car": car, "entry": entry_time})
        print(f"{car} parked at {entry_time:%H:%M}. Free places: {self.free_places}")
        return True

    def leave_parking(self, plate, exit_time=None):
        exit_time = exit_time or datetime.now()
        for record in self._cars:
            if record["car"].plate == plate:
                price = self._calc_price(record["entry"], exit_time)
                self._cars.remove(record)
                print(f"{record['car']} left at {exit_time:%H:%M}. "
                      f"To pay: {price:.2f} UAH")
                return price
        print(f"Car with plate {plate} is not in the parking.")
        return None

    def _calc_price(self, entry, exit_time):
        hours = (exit_time - entry).total_seconds() / 3600
        return max(1, math.ceil(hours)) * self._price_per_hour

    def sort_by_duration(self, now=None):
        now = now or datetime.now()
        self._cars.sort(key=lambda r: now - r["entry"], reverse=True)

    def show_parking(self, now=None):
        now = now or datetime.now()
        print(f"\n=== Parking ({len(self._cars)}/{self._max_places}), "
              f"price: {self._price_per_hour} UAH/hour ===")
        if not self._cars:
            print("Parking is empty")
            return
        for i, r in enumerate(self._cars, 1):
            minutes = int((now - r["entry"]).total_seconds() // 60)
            price = self._calc_price(r["entry"], now)
            print(f"{i}. {r['car']} | parked: {minutes // 60} h {minutes % 60} min "
                  f"| price: {price:.2f} UAH")


def main():
    now = datetime.now()

    car1 = Car(Brand.TOYOTA, 5, 200, 150, "AA1111AA")
    car2 = Car(Brand.BMW, 3, 250, 249, "BB2222BB")
    car3 = Car(Brand.AUDI, 8, 230, 190, "CC3333CC")
    car4 = Car(Brand.SKODA, 2, 210, 110, "DD4444DD")

    for c in (car1, car2, car3, car4):
        c.show_info()

    parking = Parking(max_places=3, price_per_hour=40)

    print("\n--- Parking ---")
    parking.park_car(car1, now - timedelta(hours=2, minutes=10))
    parking.park_car(car2, now - timedelta(hours=5))
    parking.park_car(car3, now - timedelta(minutes=45))
    parking.park_car(car4, now)  # no free places -> message

    print("\n--- Before sorting ---")
    parking.show_parking(now)

    print("\n--- After sorting by duration ---")
    parking.sort_by_duration(now)
    parking.show_parking(now)

    print("\n--- Leaving ---")
    parking.leave_parking("BB2222BB", now)
    parking.leave_parking("ZZ0000ZZ", now)  # not in parking
    parking.park_car(car4, now)
    parking.show_parking(now)


if __name__ == "__main__":
    main()