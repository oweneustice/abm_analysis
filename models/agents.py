import mesa
import numpy as np

class EmployeeAgent(mesa.Agent):
    """An agent representing an employee in the organization."""
    
    def __init__(self, unique_id, model, employee_type, initial_satisfaction=None):
        super().__init__(unique_id, model)
        self.employee_type = employee_type
        self.years_employed = 0
        self.salary = self._initialize_salary()
        
        # Initialize attributes based on employee type with randomness
        if employee_type == "manager":
            # Base values for managers with random variation
            self.growth_opportunities = np.random.uniform(0.1, 0.5)  # Lower with variation
            self.manager_relationship = np.random.uniform(0.6, 0.9)  # Higher with variation
            self.worklife_balance = np.random.uniform(0.3, 0.5)      # Lower with variation
        elif employee_type == "senior":
            # Base values for senior staff with random variation
            self.growth_opportunities = np.random.uniform(0.3, 0.6)  # Medium with variation
            self.manager_relationship = np.random.uniform(0.4, 0.8)  # Medium with variation
            self.worklife_balance = np.random.uniform(0.5, 0.7)      # Medium with variation
        else:  # junior
            # Base values for junior staff with random variation
            self.growth_opportunities = np.random.uniform(0.6, 0.9)  # Higher with variation
            self.manager_relationship = np.random.uniform(0.4, 0.7)  # Medium with variation
            self.worklife_balance = np.random.uniform(0.6, 0.9)      # Higher with variation
        
        # Calculate initial satisfaction based on factors if not provided
        if initial_satisfaction is None:
            self._update_satisfaction()
        else:
            self.satisfaction = initial_satisfaction
        
    def step(self):
        # Update satisfaction based on various factors
        self._update_satisfaction()
        
        # Decide whether to stay or leave
        if self._will_leave():
            self.model.schedule.remove(self)
            self.model.hire_new_employee(self.employee_type)
        else:
            self.years_employed += 1
            # Maybe get a raise or promotion based on years_employed
            self._consider_raise_or_promotion()

    def _initialize_salary(self):
        # Adjust salary ranges to match your organization
        if self.employee_type == "manager":
            return 120000 + np.random.normal(0, 12000)  # Updated values
        elif self.employee_type == "senior":
            return 85000 + np.random.normal(0, 8500)    # Updated values
        else:  # junior
            return 60000 + np.random.normal(0, 6000)    # Updated values
        
    def _update_satisfaction(self):
        # Adjust weights based on what matters most in your organization
        salary_satisfaction = min(1.0, self.salary / (120000 if self.employee_type == "junior" else 180000))
        
        # These weights should sum to 1
        self.satisfaction = (
            0.25 * salary_satisfaction +           # Changed from 0.3
            0.30 * self.growth_opportunities +     # Changed from 0.2
            0.25 * self.manager_relationship +     # Changed from 0.3
            0.20 * self.worklife_balance           # Same
        )
        
        # Add some randomness
        self.satisfaction += np.random.normal(0, 0.05)
        self.satisfaction = max(0, min(1, self.satisfaction))
    
    def _will_leave(self):
        # Probability of leaving increases as satisfaction decreases
        leave_probability = 1 - self.satisfaction
        return np.random.random() < leave_probability
    
    def _consider_raise_or_promotion(self):
        # Simplified raise/promotion logic
        if self.years_employed % 2 == 0:  # Every 2 years
            self.salary *= 1.05  # 5% raise
            self.growth_opportunities = min(1.0, self.growth_opportunities + 0.1)