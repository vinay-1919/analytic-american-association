from models.task import Task
from models.employee import Employee
from models.client import Client
from models.timesheet import TimeSheet
from models.billing import Billing

class AnalyticAmericanAssociation:
    def __init__(self):
        self.task_manager = Task()
        self.employee_manager = Employee()
        self.client_manager = Client()
        self.timesheet_manager = TimeSheet(self.task_manager, self.employee_manager, self.client_manager)
        self.billing_manager = Billing(self.task_manager, self.employee_manager, 
                                      self.client_manager, self.timesheet_manager)
    
    def initialize_sample_data(self):
        # Create sample tasks
        try:
            self.task_manager.create_from_csv('tasks.csv')
        except FileNotFoundError:
            print("No tasks.csv file found. Starting with empty task list.")
        
        # Create sample employees
        try:
            self.employee_manager.create_from_csv('employees.csv')
        except FileNotFoundError:
            print("No employees.csv file found. Starting with empty employee list.")
        
        # Create sample clients
        try:
            self.client_manager.create_from_csv('clients.csv')
        except FileNotFoundError:
            print("No clients.csv file found. Starting with empty client list.")
    
    def run(self):
        print("Welcome to Analytic American Association Management System")
        while True:
            print("\nMain Menu:")
            print("1. Task Management")
            print("2. Employee Management")
            print("3. Client Management")
            print("4. Timesheet Management")
            print("5. Billing Management")
            print("6. Exit")
            
            choice = input("Enter your choice (1-6): ")
            
            if choice == '1':
                self.task_management_menu()
            elif choice == '2':
                self.employee_management_menu()
            elif choice == '3':
                self.client_management_menu()
            elif choice == '4':
                self.timesheet_management_menu()
            elif choice == '5':
                self.billing_management_menu()
            elif choice == '6':
                print("Exiting the system. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
    
    def task_management_menu(self):
        while True:
            print("\nTask Management:")
            print("1. Create Task")
            print("2. Update Task")
            print("3. Delete Task")
            print("4. Search Task")
            print("5. List All Tasks")
            print("6. Back to Main Menu")
            
            choice = input("Enter your choice (1-6): ")
            
            if choice == '1':
                try:
                    task_name = input("Enter task name: ")
                    chargeable = input("Is this task chargeable (True/False/Yes/No): ")
                    rate_card = None
                    if chargeable.lower() in ['true', 'yes']:
                        rate_card = input("Enter rate card amount: ")
                    task_id = self.task_manager.create_task(task_name, chargeable, rate_card)
                    print(f"Task created successfully with ID: {task_id}")
                except ValueError as e:
                    print(f"Error: {e}")
            
            elif choice == '2':
                task_id = input("Enter task ID to update: ")
                try:
                    task = self.task_manager.get_by_id(task_id)
                    if not task:
                        print("Task not found.")
                        continue
                    
                    print("Leave blank to keep current value.")
                    task_name = input(f"Enter new task name [{task['task_name']}]: ") or None
                    chargeable = input(f"Is this task chargeable (True/False/Yes/No) [{task['chargeable']}]: ") or None
                    rate_card = None
                    if chargeable and chargeable.lower() in ['true', 'yes'] or (
                        not chargeable and task['chargeable'].lower() in ['true', 'yes']):
                        rate_card = input(f"Enter rate card amount [{task['rate_card']}]: ") or None
                    
                    self.task_manager.update_task(task_id, task_name, chargeable, rate_card)
                    print("Task updated successfully.")
                except ValueError as e:
                    print(f"Error: {e}")
            
            elif choice == '3':
                task_id = input("Enter task ID to delete: ")
                if self.task_manager.delete(task_id):
                    print("Task deleted successfully.")
                else:
                    print("Task not found.")
            
            elif choice == '4':
                task_id = input("Enter task ID to search: ")
                task = self.task_manager.get_by_id(task_id)
                if task:
                    print("\nTask Details:")
                    for key, value in task.items():
                        print(f"{key.replace('_', ' ').title()}: {value}")
                else:
                    print("Task not found.")
            
            elif choice == '5':
                tasks = self.task_manager.list_all()
                if tasks:
                    print("\nAll Tasks:")
                    for task in tasks:
                        print(f"ID: {task['id']}, Name: {task['task_name']}, Chargeable: {task['chargeable']}")
                else:
                    print("No tasks available in the system.")
            
            elif choice == '6':
                break
            
            else:
                print("Invalid choice. Please try again.")
    
    def employee_management_menu(self):
        while True:
            print("\nEmployee Management:")
            print("1. Create Employee")
            print("2. Update Employee")
            print("3. Delete Employee")
            print("4. Search Employee")
            print("5. List All Employees")
            print("6. Back to Main Menu")
            
            choice = input("Enter your choice (1-6): ")
            
            if choice == '1':
                try:
                    employee_name = input("Enter employee name: ")
                    std_bill_rate = input("Enter standard bill rate: ")
                    
                    print("\nEnter Address Details:")
                    mail_id = input("Email: ")
                    phone_number = input("Phone number: ")
                    house_no = input("House number: ")
                    building_number = input("Building number: ")
                    road_number = input("Road number: ")
                    street_name = input("Street name: ")
                    land_mark = input("Landmark: ")
                    city = input("City: ")
                    state = input("State: ")
                    zip_code = input("Zip code: ")
                    
                    address = Address(mail_id, phone_number, house_no, building_number, 
                                    road_number, street_name, land_mark, city, state, zip_code)
                    
                    employee_id = self.employee_manager.create_employee(employee_name, std_bill_rate, address)
                    print(f"Employee created successfully with ID: {employee_id}")
                except ValueError as e:
                    print(f"Error: {e}")
            
            elif choice == '2':
                employee_id = input("Enter employee ID to update: ")
                try:
                    employee = self.employee_manager.get_by_id(employee_id)
                    if not employee:
                        print("Employee not found.")
                        continue
                    
                    print("Leave blank to keep current value.")
                    employee_name = input(f"Enter new employee name [{employee['employee_name']}]: ") or None
                    std_bill_rate = input(f"Enter new standard bill rate [{employee['std_bill_rate']}]: ") or None
                    
                    print("\nEnter new address details (leave blank to keep current value):")
                    mail_id = input(f"Email [{employee['mail_id']}]: ") or None
                    phone_number = input(f"Phone number [{employee['phone_number']}]: ") or None
                    house_no = input(f"House number [{employee['house_no']}]: ") or None
                    building_number = input(f"Building number [{employee['building_number']}]: ") or None
                    road_number = input(f"Road number [{employee['road_number']}]: ") or None
                    street_name = input(f"Street name [{employee['street_name']}]: ") or None
                    land_mark = input(f"Landmark [{employee['land_mark']}]: ") or None
                    city = input(f"City [{employee['city']}]: ") or None
                    state = input(f"State [{employee['state']}]: ") or None
                    zip_code = input(f"Zip code [{employee['zip_code']}]: ") or None
                    
                    # Create address object only if at least one field is being updated
                    address = None
                    if any([mail_id, phone_number, house_no, building_number, road_number, 
                           street_name, land_mark, city, state, zip_code]):
                        
                        mail_id = mail_id if mail_id is not None else employee['mail_id']
                        phone_number = phone_number if phone_number is not None else employee['phone_number']
                        house_no = house_no if house_no is not None else employee['house_no']
                        building_number = building_number if building_number is not None else employee['building_number']
                        road_number = road_number if road_number is not None else employee['road_number']
                        street_name = street_name if street_name is not None else employee['street_name']
                        land_mark = land_mark if land_mark is not None else employee['land_mark']
                        city = city if city is not None else employee['city']
                        state = state if state is not None else employee['state']
                        zip_code = zip_code if zip_code is not None else employee['zip_code']
                        
                        address = Address(mail_id, phone_number, house_no, building_number, 
                                         road_number, street_name, land_mark, city, state, zip_code)
                    
                    self.employee_manager.update_employee(employee_id, employee_name, std_bill_rate, address)
                    print("Employee updated successfully.")
                except ValueError as e:
                    print(f"Error: {e}")
            
            elif choice == '3':
                employee_id = input("Enter employee ID to delete: ")
                if self.employee_manager.delete(employee_id):
                    print("Employee deleted successfully.")
                else:
                    print("Employee not found.")
            
            elif choice == '4':
                employee_id = input("Enter employee ID to search: ")
                employee = self.employee_manager.get_by_id(employee_id)
                if employee:
                    print("\nEmployee Details:")
                    for key, value in employee.items():
                        print(f"{key.replace('_', ' ').title()}: {value}")
                else:
                    print("Employee not found.")
            
            elif choice == '5':
                employees = self.employee_manager.list_all()
                if employees:
                    print("\nAll Employees:")
                    for emp in employees:
                        print(f"ID: {emp['id']}, Name: {emp['employee_name']}, Rate: ${emp['std_bill_rate']}/hr")
                else:
                    print("No employees available in the system.")
            
            elif choice == '6':
                break
            
            else:
                print("Invalid choice. Please try again.")
    
    def client_management_menu(self):
        while True:
            print("\nClient Management:")
            print("1. Create Client")
            print("2. Update Client")
            print("3. Delete Client")
            print("4. Search Client")
            print("5. List All Clients")
            print("6. Back to Main Menu")
            
            choice = input("Enter your choice (1-6): ")
            
            if choice == '1':
                try:
                    client_name = input("Enter client name: ")
                    client_description = input("Enter client description: ")
                    std_bill_rate = input("Enter standard bill rate: ")
                    
                    print("\nEnter Address Details:")
                    mail_id = input("Email: ")
                    phone_number = input("Phone number: ")
                    house_no = input("House number: ")
                    building_number = input("Building number: ")
                    road_number = input("Road number: ")
                    street_name = input("Street name: ")
                    land_mark = input("Landmark: ")
                    city = input("City: ")
                    state = input("State: ")
                    zip_code = input("Zip code: ")
                    
                    address = Address(mail_id, phone_number, house_no, building_number, 
                                    road_number, street_name, land_mark, city, state, zip_code)
                    
                    client_id = self.client_manager.create_client(client_name, client_description, std_bill_rate, address)
                    print(f"Client created successfully with ID: {client_id}")
                except ValueError as e:
                    print(f"Error: {e}")
            
            elif choice == '2':
                client_id = input("Enter client ID to update: ")
                try:
                    client = self.client_manager.get_by_id(client_id)
                    if not client:
                        print("Client not found.")
                        continue
                    
                    print("Leave blank to keep current value.")
                    client_name = input(f"Enter new client name [{client['client_name']}]: ") or None
                    client_description = input(f"Enter new client description [{client['client_description']}]: ") or None
                    std_bill_rate = input(f"Enter new standard bill rate [{client['std_bill_rate']}]: ") or None
                    
                    print("\nEnter new address details (leave blank to keep current value):")
                    mail_id = input(f"Email [{client['mail_id']}]: ") or None
                    phone_number = input(f"Phone number [{client['phone_number']}]: ") or None
                    house_no = input(f"House number [{client['house_no']}]: ") or None
                    building_number = input(f"Building number [{client['building_number']}]: ") or None
                    road_number = input(f"Road number [{client['road_number']}]: ") or None
                    street_name = input(f"Street name [{client['street_name']}]: ") or None
                    land_mark = input(f"Landmark [{client['land_mark']}]: ") or None
                    city = input(f"City [{client['city']}]: ") or None
                    state = input(f"State [{client['state']}]: ") or None
                    zip_code = input(f"Zip code [{client['zip_code']}]: ") or None
                    
                    # Create address object only if at least one field is being updated
                    address = None
                    if any([mail_id, phone_number, house_no, building_number, road_number, 
                           street_name, land_mark, city, state, zip_code]):
                        
                        mail_id = mail_id if mail_id is not None else client['mail_id']
                        phone_number = phone_number if phone_number is not None else client['phone_number']
                        house_no = house_no if house_no is not None else client['house_no']
                        building_number = building_number if building_number is not None else client['building_number']
                        road_number = road_number if road_number is not None else client['road_number']
                        street_name = street_name if street_name is not None else client['street_name']
                        land_mark = land_mark if land_mark is not None else client['land_mark']
                        city = city if city is not None else client['city']
                        state = state if state is not None else client['state']
                        zip_code = zip_code if zip_code is not None else client['zip_code']
                        
                        address = Address(mail_id, phone_number, house_no, building_number, 
                                         road_number, street_name, land_mark, city, state, zip_code)
                    
                    self.client_manager.update_client(client_id, client_name, client_description, std_bill_rate, address)
                    print("Client updated successfully.")
                except ValueError as e:
                    print(f"Error: {e}")
            
            elif choice == '3':
                client_id = input("Enter client ID to delete: ")
                if self.client_manager.delete(client_id):
                    print("Client deleted successfully.")
                else:
                    print("Client not found.")
            
            elif choice == '4':
                client_id = input("Enter client ID to search: ")
                client = self.client_manager.get_by_id(client_id)
                if client:
                    print("\nClient Details:")
                    for key, value in client.items():
                        print(f"{key.replace('_', ' ').title()}: {value}")
                else:
                    print("Client not found.")
            
            elif choice == '5':
                clients = self.client_manager.list_all()
                if clients:
                    print("\nAll Clients:")
                    for clt in clients:
                        print(f"ID: {clt['id']}, Name: {clt['client_name']}, Rate: ${clt['std_bill_rate']}/hr")
                else:
                    print("No clients available in the system.")
            
            elif choice == '6':
                break
            
            else:
                print("Invalid choice. Please try again.")
    
    def timesheet_management_menu(self):
        while True:
            print("\nTimesheet Management:")
            print("1. Create Timesheet")
            print("2. Update Timesheet")
            print("3. Search Timesheet")
            print("4. List All Timesheets")
            print("5. Back to Main Menu")
            
            choice = input("Enter your choice (1-5): ")
            
            if choice == '1':
                try:
                    timesheet_date = input("Enter timesheet date (YYYY/MM/DD): ")
                    employee_id = input("Enter employee ID: ")
                    client_id = input("Enter client ID: ")
                    task_id = input("Enter task ID: ")
                    hours = input("Enter hours worked (max 8): ")
                    
                    timesheet_id = self.timesheet_manager.create_timesheet(
                        timesheet_date, employee_id, client_id, task_id, hours
                    )
                    print(f"Timesheet created successfully with ID: {timesheet_id}")
                except ValueError as e:
                    print(f"Error: {e}")
            
            elif choice == '2':
                timesheet_id = input("Enter timesheet ID to update: ")
                try:
                    timesheet = self.timesheet_manager.get_by_id(timesheet_id)
                    if not timesheet:
                        print("Timesheet not found.")
                        continue
                    
                    print("Leave blank to keep current value.")
                    client_id = input(f"Enter new client ID [{timesheet['client_id']}]: ") or None
                    task_id = input(f"Enter new task ID [{timesheet['task_id']}]: ") or None
                    hours = input(f"Enter new hours worked [{timesheet['hours']}]: ") or None
                    
                    self.timesheet_manager.update_timesheet(timesheet_id, client_id, task_id, hours)
                    print("Timesheet updated successfully.")
                except ValueError as e:
                    print(f"Error: {e}")
            
            elif choice == '3':
                timesheet_id = input("Enter timesheet ID to search: ")
                timesheet = self.timesheet_manager.get_by_id(timesheet_id)
                if timesheet:
                    print("\nTimesheet Details:")
                    for key, value in timesheet.items():
                        print(f"{key.replace('_', ' ').title()}: {value}")
                else:
                    print("Timesheet not found.")
            
            elif choice == '4':
                timesheets = self.timesheet_manager.list_all()
                if timesheets:
                    print("\nAll Timesheets:")
                    for ts in timesheets:
                        print(f"ID: {ts['id']}, Date: {ts['timesheet_date']}, Employee: {ts['employee_id']}, "
                              f"Client: {ts['client_id']}, Task: {ts['task_id']}, Hours: {ts['hours']}")
                else:
                    print("No timesheets available in the system.")
            
            elif choice == '5':
                break
            
            else:
                print("Invalid choice. Please try again.")
    
    def billing_management_menu(self):
        while True:
            print("\nBilling Management:")
            print("1. Generate Employee Bill")
            print("2. Generate Client Bill")
            print("3. Back to Main Menu")
            
            choice = input("Enter your choice (1-3): ")
            
            if choice == '1':
                try:
                    employee_id = input("Enter employee ID: ")
                    bill_date = input("Enter bill date (YYYY/MM/DD): ")
                    bill_status = input("Enter bill status (True/False/Yes/No): ")
                    
                    filename = self.billing_manager.generate_employee_bill(employee_id, bill_date, bill_status)
                    print(f"Employee bill generated successfully: {filename}")
                except ValueError as e:
                    print(f"Error: {e}")
            
            elif choice == '2':
                try:
                    client_id = input("Enter client ID: ")
                    bill_date = input("Enter bill date (YYYY/MM/DD): ")
                    bill_status = input("Enter bill status (True/False/Yes/No): ")
                    
                    filename = self.billing_manager.generate_client_bill(client_id, bill_date, bill_status)
                    print(f"Client bill generated successfully: {filename}")
                except ValueError as e:
                    print(f"Error: {e}")
            
            elif choice == '3':
                break
            
            else:
                print("Invalid choice. Please try again.")

# Main function
if __name__ == "__main__":
    app = AnalyticAmericanAssociation()
    app.initialize_sample_data()
    app.run()