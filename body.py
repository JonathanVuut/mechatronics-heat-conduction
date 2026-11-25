class Body:
    def __init__(self,mass,heat_capacity,temperature):
        if mass<=0:
            print("Error: Mass must be greater than 0. Settin default to 1.")
            mass=1.0
        if heat_capacity<=0:
            print("Error: Heat capacity must be greater than 0. Settin default to 1.")
            heat_capacity=1.0
        if temperature<0:
            print("Error: Temperature must be 0 or higher. Settin default to 0.")
            temperature=0.0

        self.mass = mass
        self.heat_capacity=heat_capacity
        self.temperature=temperature

    def add_heat(self,heat):
        delta_t=heat/(self.mass*self.heat_capacity)
        self.temperature+=delta_t
        return self.temperature

if __name__ == "__main__":
    body1=Body(100,0.15,200)
    print(body1.add_heat(20))
    print(body1.add_heat(-40))