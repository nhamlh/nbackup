from .main import db


class Devices(db.Model):
    __tablename__ = 'devices'
    id = db.Column(db.Integer, primary_key=True)
    IP = db.Column(db.String(15), primary_key=True)
    hostname = db.Column(db.String(350))
    device_type = db.Column(db.String(20))  # currently support cisco, juniper
    group_id = db.Column(db.Integer, db.ForeignKey('devicegroups.id'))
    active = db.Column(db.Boolean)  # don't backup this device if False
    login_by_ssh = db.Column(db.Boolean)  # use telnet if login_by_ssh is False
    last_update = db.Column(db.Date)

    def __repr__(self):
        return '{0}: {1}'.format(self.device_type, self.hostname)


class DeviceGroups(db.Model):
    __tablename__ = 'devicegroups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(350))
    devices = db.relationship('Devices', backref='group', lazy='dynamic')
    backup_frequency = db.Column(db.Integer) # 0: daily, 1: weekly, 2: monthly

    def __repr__(self):
        return 'group {}'.format(self.name)


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), primary_key=True)
    password = db.Column(db.String(20))
    read_only = db.Column(db.Boolean)

    def __repr__(self):
        return 'user {}'.format(self.username)
