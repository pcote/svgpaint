from sqlalchemy import create_engine, Column, Text, Integer, VARCHAR, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from configparser import ConfigParser
import os
from flask_login import UserMixin

# ENGINE SETUP
this_directory = __file__.rsplit(os.path.sep, maxsplit=1)[0]
config_file_path = "{}{}config.ini".format(this_directory, os.path.sep)
cp = ConfigParser()
cp.read(config_file_path)
config_sec = cp["dbconfig"]
user = config_sec.get("username")
pw = config_sec.get("password")
db_url = "mysql+pymysql://{}:{}@localhost/svgpaint".format(user, pw)
eng = create_engine(db_url)


Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    username = Column(VARCHAR(50), primary_key=True, nullable=False)
    password = Column(Text, nullable=False)
    is_active = Column(Boolean, default=False)
    is_authenticated = Column(Boolean, default=False)
    is_anonymous = Column(Boolean, default=False)
    drawings = relationship("Drawing")

    def get_id(self):
        return self.username


class Drawing(Base):
    __tablename__ = "drawings"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(50))
    user = Column(ForeignKey("users.username"))


Session = sessionmaker(bind=eng)
Base.metadata.create_all(eng)


def create_drawing(drawing_name, uid):
    sess = Session()
    drawing = Drawing(name=drawing_name, user=uid)
    sess.add(drawing)
    sess.commit()
    sess.close()

def create_user(uname, pw):
    sess = Session()
    user = User(username=uname, password=pw)
    sess.add(user)
    sess.commit()
    sess.close()


def get_user(uname):
    sess = Session()
    user = sess.query(User).filter_by(username=uname).one_or_none()
    sess.close()
    return user


def get_drawings(uid):
    sess = Session()
    user = sess.query(User).filter_by(username=uid).one_or_none()
    drawings = user.drawings
    sess.close()
    return drawings


def is_password_valid(uname, pw):
    user = get_user(uname)
    if user and user.password == pw:
        return True
    return False


def set_authenticate(uname, auth_status):
    sess = Session()
    user = get_user(uname)
    user.is_authenticated = auth_status
    sess.add(user)
    sess.commit()
    sess.close()

if __name__ == '__main__':
    print("okay, check the database for status of tables.")