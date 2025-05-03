from utils.validators import validate_email, validate_phone, validate_address_field, validate_alphabets, validate_zip_code

# Address Class
class Address:
    def __init__(self, mail_id, phone_number, house_no, building_number, road_number, 
                 street_name, land_mark, city, state, zip_code):
        validate_email(mail_id)
        validate_phone(phone_number)
        validate_address_field(house_no, "house number")
        validate_address_field(building_number, "building number")
        validate_address_field(road_number, "road number")
        validate_address_field(street_name, "street name")
        validate_address_field(land_mark, "landmark")
        validate_alphabets(city, "city")
        validate_alphabets(state, "state")
        validate_zip_code(zip_code)
        
        self.mail_id = mail_id
        self.phone_number = phone_number
        self.house_no = house_no
        self.building_number = building_number
        self.road_number = road_number
        self.street_name = street_name
        self.land_mark = land_mark
        self.city = city
        self.state = state
        self.zip_code = zip_code
    
    def to_dict(self):
        return {
            'mail_id': self.mail_id,
            'phone_number': self.phone_number,
            'house_no': self.house_no,
            'building_number': self.building_number,
            'road_number': self.road_number,
            'street_name': self.street_name,
            'land_mark': self.land_mark,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            data['mail_id'],
            data['phone_number'],
            data['house_no'],
            data['building_number'],
            data['road_number'],
            data['street_name'],
            data['land_mark'],
            data['city'],
            data['state'],
            data['zip_code']
        )