from sqlalchemy import create_engine, Column, Text, Integer, VARCHAR, Boolean
from sqlalchemy.orm import sessionmaker
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
    username = Column(Text, primary_key=True, nullable=False)
    password = Column(Text, nullable=False)
    is_active = Column(Boolean, default=False)
    is_authenticated = Column(Boolean, default=False)
    is_anonymous = Column(Boolean, default=False)

    def get_id(self):
        return self.username


Session = sessionmaker(bind=eng)
Base.metadata.create_all(eng)


def create_user(uname, pw):
    sess = Session()
    user = User(username=uname, password=pw)
    sess.add(user)
    sess.commit()


def get_user(uname):
    sess = Session()
    user = sess.query(User).filter_by(username=uname).one_or_none()
    return user


if __name__ == '__main__':
    sess = Session()
    user = User(username="cotejrp", password="rosebud")
    sess.add(user)
    sess.commit()