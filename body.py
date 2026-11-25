class Body:
    def __init__(self,mass,heat_capacity,temprature):
        if mass<=0:
            print("Error: Mass must be greater than 0. Settin default to 1.")
            mass=1.0
        if heat_capacity<=0:
            print("Error: Heat capacity must be greater than 0. Settin default to 1.")
            heat_capacity=1.0
        if temprature<0:
            print("Error: Temprature must be greater than 0. Settin default to 0.")
            temprature=0.0

        self.mass = mass
        self.heat_capacity=heat_capacity
        self.temprature=temprature