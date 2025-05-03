import random
from models.base_entity import Entity
from utils.validators import validate_name, validate_chargeable

# Task Management
class Task(Entity):
    def __init__(self):
        super().__init__()
        self.file_name = "tasks.csv"
        self.load_from_file()
    
    def generate_id(self):
        return f"TSK_{random.randint(100000, 999999)}"
    
    def create_task(self, task_name, chargeable, rate_card=None):
        validate_name(task_name, "task name")
        validate_chargeable(chargeable)
        
        chargeable = chargeable.lower() in ['true', 'yes']
        
        if chargeable and rate_card is None:
            raise ValueError("Rate card is required for chargeable tasks.")
        
        if chargeable:
            try:
                rate_card = float(rate_card)
                if rate_card <= 0:
                    raise ValueError("Rate card must be positive.")
            except ValueError:
                raise ValueError("Rate card must be a number.")
        
        task_id = self.generate_id()
        task = {
            'id': task_id,
            'task_name': task_name,
            'chargeable': str(chargeable),
            'rate_card': str(rate_card) if chargeable else '0'
        }
        
        self.entities.append(task)
        self.save_to_file()
        return task_id
    
    def update_task(self, task_id, task_name=None, chargeable=None, rate_card=None):
        task = self.get_by_id(task_id)
        if not task:
            raise ValueError("Task not found.")
        
        if task_name is not None:
            validate_name(task_name, "task name")
            task['task_name'] = task_name
        
        if chargeable is not None:
            validate_chargeable(chargeable)
            new_chargeable = chargeable.lower() in ['true', 'yes']
            task['chargeable'] = str(new_chargeable)
            
            if new_chargeable and rate_card is None and task['rate_card'] == '0':
                raise ValueError("Rate card is required for chargeable tasks.")
        
        if rate_card is not None:
            if task['chargeable'].lower() == 'false':
                raise ValueError("Cannot set rate card for non-chargeable task.")
            
            try:
                rate_card = float(rate_card)
                if rate_card <= 0:
                    raise ValueError("Rate card must be positive.")
                task['rate_card'] = str(rate_card)
            except ValueError:
                raise ValueError("Rate card must be a number.")
        
        self.save_to_file()
        return True
    
    def create_from_csv(self, csv_file):
        try:
            with open(csv_file, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    try:
                        self.create_task(
                            row['task_name'],
                            row['chargeable'],
                            row.get('rate_card')
                        )
                    except ValueError as e:
                        print(f"Skipping invalid task data: {e}")
        except FileNotFoundError:
            raise FileNotFoundError("CSV file not found.")
        except Exception as e:
            raise Exception(f"Error reading CSV file: {e}")