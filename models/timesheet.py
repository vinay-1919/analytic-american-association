import random
from models.base_entity import Entity
from utils.validators import validate_date, validate_hours

# Timesheet Management
class TimeSheet(Entity):
    def __init__(self, task_manager, employee_manager, client_manager):
        super().__init__()
        self.file_name = "timesheets.csv"
        self.task_manager = task_manager
        self.employee_manager = employee_manager
        self.client_manager = client_manager
        self.load_from_file()
    
    def generate_id(self):
        return f"TMS_{random.randint(100000, 999999)}"
    
    def create_timesheet(self, timesheet_date, employee_id, client_id, task_id, hours):
        validate_date(timesheet_date)
        validate_hours(hours)
        
        if not self.employee_manager.get_by_id(employee_id):
            raise ValueError("Employee not found.")
        
        if not self.client_manager.get_by_id(client_id):
            raise ValueError("Client not found.")
        
        if not self.task_manager.get_by_id(task_id):
            raise ValueError("Task not found.")
        
        timesheet_id = self.generate_id()
        timesheet = {
            'id': timesheet_id,
            'timesheet_date': timesheet_date,
            'employee_id': employee_id,
            'client_id': client_id,
            'task_id': task_id,
            'hours': str(hours)
        }
        
        self.entities.append(timesheet)
        self.save_to_file()
        return timesheet_id
    
    def update_timesheet(self, timesheet_id, client_id=None, task_id=None, hours=None):
        timesheet = self.get_by_id(timesheet_id)
        if not timesheet:
            raise ValueError("Timesheet not found.")
        
        if client_id is not None:
            if not self.client_manager.get_by_id(client_id):
                raise ValueError("Client not found.")
            timesheet['client_id'] = client_id
        
        if task_id is not None:
            if not self.task_manager.get_by_id(task_id):
                raise ValueError("Task not found.")
            timesheet['task_id'] = task_id
        
        if hours is not None:
            validate_hours(hours)
            timesheet['hours'] = str(hours)
        
        self.save_to_file()
        return True
    
    def get_timesheets_by_employee(self, employee_id):
        return [ts for ts in self.entities if ts['employee_id'] == employee_id]
    
    def get_timesheets_by_client(self, client_id):
        return [ts for ts in self.entities if ts['client_id'] == client_id]