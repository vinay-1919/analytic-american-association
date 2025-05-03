from utils.validators import validate_date, validate_chargeable

# Billing Management
class Billing:
    def __init__(self, task_manager, employee_manager, client_manager, timesheet_manager):
        self.task_manager = task_manager
        self.employee_manager = employee_manager
        self.client_manager = client_manager
        self.timesheet_manager = timesheet_manager
    
    def generate_employee_bill(self, employee_id, bill_date, bill_status):
        validate_date(bill_date)
        validate_chargeable(bill_status)
        
        employee = self.employee_manager.get_by_id(employee_id)
        if not employee:
            raise ValueError("Employee not found.")
        
        timesheets = self.timesheet_manager.get_timesheets_by_employee(employee_id)
        if not timesheets:
            raise ValueError("No timesheets found for this employee.")
        
        total_hours = 0
        total_amount = 0
        bill_details = []
        
        for ts in timesheets:
            task = self.task_manager.get_by_id(ts['task_id'])
            if task and task['chargeable'].lower() in ['true', 'yes']:
                hours = float(ts['hours'])
                rate = float(employee['std_bill_rate'])
                amount = hours * rate
                
                total_hours += hours
                total_amount += amount
                
                bill_details.append({
                    'date': ts['timesheet_date'],
                    'client': self.client_manager.get_by_id(ts['client_id'])['client_name'],
                    'task': task['task_name'],
                    'hours': hours,
                    'rate': rate,
                    'amount': amount
                })
        
        if not bill_details:
            raise ValueError("No chargeable timesheets found for this employee.")
        
        # Generate bill text
        bill_text = f"Employee Bill\n"
        bill_text += f"Generated Date: {bill_date}\n"
        bill_text += f"Employee ID: {employee_id}\n"
        bill_text += f"Employee Name: {employee['employee_name']}\n"
        bill_text += f"Standard Rate: ${employee['std_bill_rate']}/hr\n"
        bill_text += f"Status: {'Paid' if bill_status.lower() in ['true', 'yes'] else 'Pending'}\n\n"
        bill_text += "Details:\n"
        
        for detail in bill_details:
            bill_text += (f"Date: {detail['date']}, Client: {detail['client']}, "
                         f"Task: {detail['task']}, Hours: {detail['hours']}, "
                         f"Rate: ${detail['rate']}, Amount: ${detail['amount']:.2f}\n")
        
        bill_text += f"\nTotal Hours: {total_hours}\n"
        bill_text += f"Total Amount: ${total_amount:.2f}\n"
        
        # Save to file
        filename = f"employee_bill_{employee_id}_{bill_date.replace('/', '-')}.txt"
        with open(filename, 'w') as file:
            file.write(bill_text)
        
        return filename
    
    def generate_client_bill(self, client_id, bill_date, bill_status):
        validate_date(bill_date)
        validate_chargeable(bill_status)
        
        client = self.client_manager.get_by_id(client_id)
        if not client:
            raise ValueError("Client not found.")
        
        timesheets = self.timesheet_manager.get_timesheets_by_client(client_id)
        if not timesheets:
            raise ValueError("No timesheets found for this client.")
        
        total_hours = 0
        total_amount = 0
        bill_details = []
        
        for ts in timesheets:
            task = self.task_manager.get_by_id(ts['task_id'])
            employee = self.employee_manager.get_by_id(ts['employee_id'])
            
            if task and task['chargeable'].lower() in ['true', 'yes'] and employee:
                hours = float(ts['hours'])
                rate = float(client['std_bill_rate'])
                amount = hours * rate
                
                total_hours += hours
                total_amount += amount
                
                bill_details.append({
                    'date': ts['timesheet_date'],
                    'employee': employee['employee_name'],
                    'task': task['task_name'],
                    'hours': hours,
                    'rate': rate,
                    'amount': amount
                })
        
        if not bill_details:
            raise ValueError("No chargeable timesheets found for this client.")
        
        # Generate bill text
        bill_text = f"Client Bill\n"
        bill_text += f"Generated Date: {bill_date}\n"
        bill_text += f"Client ID: {client_id}\n"
        bill_text += f"Client Name: {client['client_name']}\n"
        bill_text += f"Standard Rate: ${client['std_bill_rate']}/hr\n"
        bill_text += f"Status: {'Paid' if bill_status.lower() in ['true', 'yes'] else 'Pending'}\n\n"
        bill_text += "Details:\n"
        
        for detail in bill_details:
            bill_text += (f"Date: {detail['date']}, Employee: {detail['employee']}, "
                         f"Task: {detail['task']}, Hours: {detail['hours']}, "
                         f"Rate: ${detail['rate']}, Amount: ${detail['amount']:.2f}\n")
        
        bill_text += f"\nTotal Hours: {total_hours}\n"
        bill_text += f"Total Amount: ${total_amount:.2f}\n"
        
        # Save to file
        filename = f"client_bill_{client_id}_{bill_date.replace('/', '-')}.txt"
        with open(filename, 'w') as file:
            file.write(bill_text)
        
        return filename