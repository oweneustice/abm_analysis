import mesa
import numpy as np
from .agents import EmployeeAgent

class OrganizationModel(mesa.Model):
    """A model representing an organization with employees."""
    
    def __init__(self, num_managers=5, num_senior=20, num_junior=50):
        super().__init__()
        self.schedule = mesa.time.RandomActivation(self)
        self.num_managers = num_managers
        self.num_senior = num_senior
        self.num_junior = num_junior
        
        # Initialize employees
        self._create_initial_employees()
        
        # Set up data collection
        self.datacollector = mesa.DataCollector(
            model_reporters={
                "Retention_Rate": self._calculate_retention_rate,
                "Average_Satisfaction": self._calculate_avg_satisfaction,
                "Manager_Count": lambda m: sum(1 for agent in m.schedule.agents if agent.employee_type == "manager"),
                "Senior_Count": lambda m: sum(1 for agent in m.schedule.agents if agent.employee_type == "senior"),
                "Junior_Count": lambda m: sum(1 for agent in m.schedule.agents if agent.employee_type == "junior"),
            },
            agent_reporters={
                "Type": "employee_type",
                "Satisfaction": "satisfaction",
                "Salary": "salary",
                "Years_Employed": "years_employed"
            }
        )
    
    def _create_initial_employees(self):
        # Create initial employees
        employee_id = 0
        
        # Create managers
        for i in range(self.num_managers):
            employee = EmployeeAgent(employee_id, self, "manager")
            self.schedule.add(employee)
            employee_id += 1
        
        # Create senior employees
        for i in range(self.num_senior):
            employee = EmployeeAgent(employee_id, self, "senior")
            self.schedule.add(employee)
            employee_id += 1
        
        # Create junior employees
        for i in range(self.num_junior):
            employee = EmployeeAgent(employee_id, self, "junior")
            self.schedule.add(employee)
            employee_id += 1
    
    def hire_new_employee(self, employee_type):
        # Create a new employee to replace one that left
        new_id = max(agent.unique_id for agent in self.schedule.agents) + 1
        new_employee = EmployeeAgent(new_id, self, employee_type)
        self.schedule.add(new_employee)
    
    def step(self):
        # Collect data
        self.datacollector.collect(self)
        
        # Execute step for all agents
        self.schedule.step()
    
    def _calculate_retention_rate(self):
        # Simple retention rate calculation
        total_employees = len(self.schedule.agents)
        replaced_employees = sum(1 for agent in self.schedule.agents if agent.years_employed == 0)
        if total_employees == 0:
            return 0
        return 1 - (replaced_employees / total_employees)
    
    def _calculate_avg_satisfaction(self):
        # Calculate average satisfaction across all employees
        if not self.schedule.agents:
            return 0
        return sum(agent.satisfaction for agent in self.schedule.agents) / len(self.schedule.agents)