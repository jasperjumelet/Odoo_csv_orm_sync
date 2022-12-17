from odoo import fields, models

class ContentModel(models.Model):
    _name = "content.model"
    _description = "this is content model"

    id = fields.Integer('ID')
    name= fields.Char("name", size=100)
    description = fields.Char("Description", size=128)
    device = fields.Many2one(comodel_name='device.model', string='Device')
    expire_date = fields.Datetime("Expire date") 
    state = fields.Selection(selection=[
        ("enabled", "enabled"),
        ("disabled", "disabled"),
        ("deleted", "deleted"),
        ],
        string="state",)


    def store_to_content_model(self, path="etc/odoo/storage/content.csv", delimeter=","):
        """
        Method to store csv content into database using ORM.
        
        args: 
            path: for csv file path
            delimeter: for csv file delimeter
        """
        import csv
        from datetime import datetime
        import logging
        logging.basicConfig(filemode="w", level=logging.DEBUG)

        with open(path) as file:
            csvreader = csv.reader(file, delimiter=delimeter)
            for row in csvreader:
                
                #datetime conversion
                try:
                    input_string = row[4]
                    format_string = '%Y-%m-%d %H:%M:%S'
                    dt = datetime.strptime(input_string, format_string)
                    logging.info("Datetime conversion successfull")

                except Exception as e:
                    logging.error(e, "time conversion error")

                # State definition
                try:
                    if dt < datetime.now():
                        state = "disabled"
                    else:
                        state = row[5]
                    logging.info("state definition successfull")
                except Exception as e:
                    logging.error(e, "failed state definition")

                # create to model
                try:
                    data = {
                            'id': row[0],
                            'name': row[1],
                            'description': row[2],
                            'device': row[3],
                            'expire_date': dt,
                            'state':  state
                            }
                    self.create(data)
                except Exception as e:
                    logging.error(e, "Import error or (item missing)")

    def to_csv(self):
        """
        Make csv from all db records 
        """
        import csv
        import re
        import logging
        logging.basicConfig(level=logging.DEBUG)
        fields=["id", "name", "description", "device", "expire_date", "state"]
        records = self.env['content.model'].search([])
        with open("etc/odoo/storage/content.csv", "w") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fields)
            content_data = []#
            for record in records:
                # get only device number using regex
                device_no = re.findall(r"\d+", str(record.device))

                content_data.append({
                    "id": record.id,
                    "name": record.name,
                    "description": record.description,
                    "device": device_no[0],
                    "expire_date": record.expire_date,
                    "state": record.state,
                    })
            writer.writerows(content_data)


