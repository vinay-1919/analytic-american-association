import random
from models.base_entity import Entity
from models.address import Address
from utils.validators import validate_name

# Client Management
class Client(Entity):
    def __init__(self):
        super().__init__()
        self.file_name = "clients.csv"
        self.load_from_file()
    
    def generate_id(self):
        return f"CLT_{random.randint(100000, 999999)}"
    
    def create_client(self, client_name, client_description, std_bill_rate, address):
        validate_name(client_name, "client name")
        validate_name(client_description, "client description")
        
        try:
            std_bill_rate = float(std_bill_rate)
            if std_bill_rate <= 0:
                raise ValueError("Standard bill rate must be positive.")
        except ValueError:
            raise ValueError("Standard bill rate must be a number.")
        
        if not isinstance(address, Address):
            raise ValueError("Invalid address object.")
        
        client_id = self.generate_id()
        client = {
            'id': client_id,
            'client_name': client_name,
            'client_description': client_description,
            'std_bill_rate': str(std_bill_rate),
            **address.to_dict()
        }
        
        self.entities.append(client)
        self.save_to_file()
        return client_id
    
    def update_client(self, client_id, client_name=None, client_description=None, std_bill_rate=None, address=None):
        client = self.get_by_id(client_id)
        if not client:
            raise ValueError("Client not found.")
        
        if client_name is not None:
            validate_name(client_name, "client name")
            client['client_name'] = client_name
        
        if client_description is not None:
            validate_name(client_description, "client description")
            client['client_description'] = client_description
        
        if std_bill_rate is not None:
            try:
                std_bill_rate = float(std_bill_rate)
                if std_bill_rate <= 0:
                    raise ValueError("Standard bill rate must be positive.")
                client['std_bill_rate'] = str(std_bill_rate)
            except ValueError:
                raise ValueError("Standard bill rate must be a number.")
        
        if address is not None:
            if not isinstance(address, Address):
                raise ValueError("Invalid address object.")
            
            address_dict = address.to_dict()
            for key in address_dict:
                client[key] = address_dict[key]
        
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
                        self.create_client(
                            row['client_name'],
                            row['client_description'],
                            row['std_bill_rate'],
                            address
                        )
                    except ValueError as e:
                        print(f"Skipping invalid client data: {e}")
        except FileNotFoundError:
            raise FileNotFoundError("CSV file not found.")
        except Exception as e:
            raise Exception(f"Error reading CSV file: {e}")