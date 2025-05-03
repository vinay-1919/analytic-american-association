from abc import ABC, abstractmethod
import os
import csv

# Base Entity Class
class Entity(ABC):
    def __init__(self):
        self.entities = []
        self.file_name = ""
    
    @abstractmethod
    def generate_id(self):
        pass
    
    def load_from_file(self):
        if os.path.exists(self.file_name):
            with open(self.file_name, 'r') as file:
                reader = csv.DictReader(file)
                self.entities = list(reader)
    
    def save_to_file(self):
        if not self.entities:
            return
        
        fieldnames = self.entities[0].keys()
        with open(self.file_name, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.entities)
    
    def get_by_id(self, entity_id):
        for entity in self.entities:
            if entity['id'] == entity_id:
                return entity
        return None
    
    def delete(self, entity_id):
        entity = self.get_by_id(entity_id)
        if entity:
            self.entities.remove(entity)
            self.save_to_file()
            return True
        return False
    
    def list_all(self):
        return self.entities