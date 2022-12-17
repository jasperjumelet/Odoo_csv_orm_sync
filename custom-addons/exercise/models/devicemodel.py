from odoo import fields, models, api
from datetime import datetime


class DeviceModel(models.Model):
    _name = "device.model"
    _description = "the device model for devices"

    id = fields.Integer('ID')
    name = fields.Char('Name', size=32)
    description = fields.Char('Description', size=128)
    code = fields.Char('code', size=128)
    expire_date = fields.Datetime("Expire date")


        
    def store_to_device_model(self, path="etc/odoo/storage/devices.csv", delimeter=","):
        """
        Import csv file to database using orm
        args:
            path: filepath to csv file
            delimeter: delimiter to read csv
        """
        import csv
        from datetime import datetime
        import logging
        logging.basicConfig(filemode="w", level=logging.DEBUG)
        

        with open(path) as file:
            csvreader = csv.reader(file, delimiter=delimeter)
            for row in csvreader:
                try:
                    # datetime conversion
                    input_string = row[4]
                    format_string = '%Y-%m-%d %H:%M:%S'
                    dt = datetime.strptime(input_string, format_string)
                except Exception as e:
                    logging.error(e, "datetime conversion error")

                # check if code already exists in code field if so leave code field empty
                code = row[3]
                code_exists = self.env['device.model'].search([('code' '!=', row[3])])
                if code_exists:
                    logging.warning("Already found code field in database: setting code to empty")
                    code = ""

                # import the data into the orm database
                try:
                    data = {
                        'id': row[0],
                        'name': row[1],
                        'description': row[2],
                        'code': code, 
                        'expire_date': dt 
                        }
                    self.create(data)
                    logging.info("import devices successfull")
                except Exception as e:
                    logging.error(e, "Item missing or conversion error")
                # print(dt, type(dt))

    

    def to_csv(self):    
        """
        Action function to store all db records to csv
        """
        import csv
        fields=["id", "name", "description", "code", "expire_date"]
        records = self.env['device.model'].search([])
        with open("etc/odoo/storage/devices.csv", 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fields)
            # writer.writeheader()
            device_data = []
            for record in records:
                device_data.append({
                    "id": record.id,
                    "name": record.name,
                    "description": record.description,
                    "code": record.code,
                    "expire_date": record.expire_date
                    })
            writer.writerows(device_data)
