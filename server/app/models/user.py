from app import app, db
from passlib.apps import custom_app_context as pw_context
from datetime import datetime
from tip import Tip
import uuid
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column('id', db.String(length=64), unique=True, nullable=False,
            primary_key=True)
    name = db.Column('name', db.String(length=64), nullable=False)
    email = db.Column('email', db.String(length=256), unique=True,
            nullable=False)
    hashed_password = db.Column('hashed_password', db.String(length=256),
            nullable=False)
    auth_token = db.Column('auth_token', db.String(length=64), unique=True)
    last_login = db.Column('last_login', db.DateTime())
    role = db.Column('role', db.String(16))

    __mapper_args__ = {
        'polymorphic_identity' : 'User',
        'polymorphic_on' : role
    }

    def __init__(self, name, email, password):
        #TODO check for valid email address
        #TODO check for valid password?
        self.id = str(uuid.uuid4())
        self.name = name
        self.email = email
        self.hashed_password = pw_context.encrypt(password)

    def __repr__(self):
        return '<{} {}>'.format(self.role, self.id)

    def json_dict(self, authed=False):
        ret = {
            'uid' : self.id,
            'email' : self.email,
            'name' : self.name
        }
        if authed:
            ret['token'] = self.auth_token

        return ret

    def hash_password(self, password):
        self.hashed_password = pw_context.encrypt(password)

    def verify_password(self, password):
        return pw_context.verify(password, self.hashed_password)

    def set_auth_token(self):
        self.auth_token = str(uuid.uuid4())
        self.last_login = datetime.utcnow()
        return self.auth_token

    def unset_auth_token(self):
        self.auth_token = None

    def serialized_token(self, expiration=1800):
        s = Serializer(app.config['SECRET_KEY'], expiration)
        return s.dumps({ 'user' : self.id }).decode('utf-8')

    @staticmethod
    def verify_serialized_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None

        uid = data.get('user')
        if uid:
            return User.query.get(uid)
        return None

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

class Admin(User):
    __tablename__ = 'admins'
    id = db.Column('id', db.String(length=64), db.ForeignKey('users.id'),
            primary_key=True)

    __mapper_args__ = { 'polymorphic_identity' : 'Admin' }

    def __init__(self, name, email, password):        
        super(Admin, self).__init__(name, email, password)

class Employee(User):
    __tablename__ = 'employees'
    id = db.Column('id', db.String(length=64), db.ForeignKey('users.id'),
            primary_key=True)    

    __mapper_args__ = { 'polymorphic_identity' : 'Employee' }

    tips = db.relationship('Tip', foreign_keys='Tip.employee_id',
            lazy='dynamic', backref='employee')

    def __init__(self, name, email, password):
        super(Employee, self).__init__(name, email, password)        