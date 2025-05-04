from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule, TextElement
from mesa.visualization.UserParam import UserSettableParameter
from .model import OrganizationModel

class ModelInfo(TextElement):
    """Display key model information in the visualization."""
    
    def render(self, model):
        if model.schedule.steps == 0 or len(model.datacollector.get_model_vars_dataframe()) == 0:
            # No data yet, first step
            return f"Step: {model.schedule.steps}<br>" \
                   f"Total Employees: {len(model.schedule.agents)}<br>" \
                   f"Retention Rate: N/A<br>" \
                   f"Avg Satisfaction: N/A"
        else:
            # We have data, safe to access
            return f"Step: {model.schedule.steps}<br>" \
                   f"Total Employees: {len(model.schedule.agents)}<br>" \
                   f"Retention Rate: {model.datacollector.get_model_vars_dataframe().iloc[-1]['Retention_Rate']:.2f}<br>" \
                   f"Avg Satisfaction: {model.datacollector.get_model_vars_dataframe().iloc[-1]['Average_Satisfaction']:.2f}"
        
def create_server():
    """Create a Mesa ModularServer with adjustable parameters."""
    
    # Define charts for tracking metrics (same as before)
    retention_chart = ChartModule([
        {"Label": "Retention_Rate", "Color": "blue"},
        {"Label": "Average_Satisfaction", "Color": "red"}
    ], data_collector_name='datacollector')
    
    employee_chart = ChartModule([
        {"Label": "Manager_Count", "Color": "green"},
        {"Label": "Senior_Count", "Color": "blue"},
        {"Label": "Junior_Count", "Color": "red"}
    ], data_collector_name='datacollector')
    
    model_info = ModelInfo()
    
    # Define user-adjustable parameters
    model_params = {
        "num_managers": UserSettableParameter(
            "slider", 
            "Number of Managers", 
            5, 1, 10, 1,
            description="Number of managers in the organization"
        ),
        "num_senior": UserSettableParameter(
            "slider", 
            "Number of Senior Staff", 
            20, 5, 50, 5,
            description="Number of senior staff in the organization"
        ),
        "num_junior": UserSettableParameter(
            "slider", 
            "Number of Junior Staff", 
            50, 10, 100, 10,
            description="Number of junior staff in the organization"
        )
    }
    
    # Create and return the server
    server = ModularServer(
        OrganizationModel,
        [model_info, retention_chart, employee_chart],
        "Employee Retention Model",
        model_params
    )
    
    server.port = 8521
    return server