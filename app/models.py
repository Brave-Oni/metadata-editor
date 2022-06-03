from . import db


class DeviceType(db.Model):
    __tablename__ = "DeviceType"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<DeviceType [{self.id}]: {self.name}>"


class Companies(db.Model):
    __tablename__ = "Companies"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<Company [{self.id}]: Name - {self.name}>"


class Devices(db.Model):
    __tablename__ = "Devices"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique=True)
    company_id = db.Column(db.ForeignKey("Companies.id"), nullable=False)
    device_type_id = db.Column(db.ForeignKey("DeviceType.id"), nullable=False)

    company = db.relationship("Companies", backref=db.backref("Devices", lazy=True))
    device_type = db.relationship("DeviceType", backref=db.backref("Devices", lazy=True))

    def __init__(self, name, company, device_type):
        self.name = name
        self.company = company
        self.device_type = device_type

    def __repr__(self):
        return f"Device [{self.id}] : Company - {self.company} Model - {self.name} Type - {self.device_type}"
