import random
from models.base_entity import Entity
from models.address import Address
from utils.validators import validate_name

# Employee Management
class Employee(Entity):
    def __init__(self):
        super().__init__()
        self.file_name = "employees.csv"
        self.load_from_file()
    
    def generate_id(self):
        return f"EMP_{random.randint(100000, 999999)}"
    
    def create_employee(self, employee_name, std_bill_rate, address):
        validate_name(employee_name, "employee name")
        
        try:
            std_bill_rate = float(std_bill_rate)
            if std_bill_rate <= 0:
                raise ValueError("Standard bill rate must be positive.")
        except ValueError:
            raise ValueError("Standard bill rate must be a number.")
        
        if not isinstance(address, Address):
            raise ValueError("Invalid address object.")
        
        employee_id = self.generate_id()
        employee = {
            'id': employee_id,
            'employee_name': employee_name,
            'std_bill_rate': str(std_bill_rate),
            **address.to_dict()
        }
        
        self.entities.append(employee)
        self.save_to_file()
        return employee_id
    
    def update_employee(self, employee_id, employee_name=None, std_bill_rate=None, address=None):
        employee = self.get_by_id(employee_id)
        if not employee:
            raise ValueError("Employee not found.")
        
        if employee_name is not None:
            validate_name(employee_name, "employee name")
            employee['employee_name'] = employee_name
        
        if std_bill_rate is not None:
            try:
                std_bill_rate = float(std_bill_rate)
                if std_bill_rate <= 0:
                    raise ValueError("Standard bill rate must be positive.")
                employee['std_bill_rate'] = str(std_bill_rate)
            except ValueError:
                raise ValueError("Standard bill rate must be a number.")
        
        if address is not None:
            if not isinstance(address, Address):
                raise ValueError("Invalid address object.")
            
            address_dict = address.to_dict()
            for key in address_dict:
                employee[key] = address_dict[key]
        
        self.save_to_file()
        return True
    
    def create_from_csv(self, csv_file):
        try:
            with open(csv_file, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    try:
                        address = Address(
                            row['mail_id'],
                            row['phone_number'],
                            row['house_no'],
                            row['building_number'],
                            row['road_number'],
                            row['street_name'],
                            row['land_mark'],
                            row['city'],
                            row['state'],
                            row['zip_code']
                        )
                        self.create_employee(
                            row['employee_name'],
                            row['std_bill_rate'],
                            address
                        )
                    except ValueError as e:
                        print(f"Skipping invalid employee data: {e}")
        except FileNotFoundError:
            raise FileNotFoundError("CSV file not found.")
        except Exception as e:
            raise Exception(f"Error reading CSV file: {e}")
