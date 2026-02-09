class Employee:
    def __init__(self, name, base_salary):
        self.name = name
        self.base_salary = base_salary
    
    def total_salary(self):
        return self.base_salary

class Manager(Employee):
    def __init__(self, name, base_salary, bonus_percent):
        super().__init__(name, base_salary)
        self.bonus_percent = bonus_percent
    
    def total_salary(self):
        return self.base_salary * (1 + self.bonus_percent / 100)

class Developer(Employee):
    def __init__(self, name, base_salary, completed_projects):
        super().__init__(name, base_salary)
        self.completed_projects = completed_projects
    
    def total_salary(self):
        return self.base_salary + self.completed_projects * 500

#intern subclass
class Intern(Employee):
    pass #inherits from employee

data = input().split()
role = data[0]
name = data[1]
base_salary = int(data[2])

if role == "Manager":
    bonus_percent = int(data[3])
    employee = Manager(name, base_salary, bonus_percent)
elif role == "Developer":
    completed_projects = int(data[3])
    employee = Developer(name, base_salary, completed_projects)
elif role == "Intern":
    employee = Intern(name, base_salary)

print(f"Name: {employee.name}, Total: {employee.total_salary():.2f}")