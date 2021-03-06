from sqlalchemy import create_engine, Column, Text, Integer, VARCHAR, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from configparser import ConfigParser
import os
import hashlib
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
    pixels = relationship("BrushPixel")


class BrushPixel(Base):
    __tablename__ = "brushpixels"
    id = Column(Integer, primary_key=True, autoincrement=True)
    color = Column(VARCHAR(25), nullable=False)
    shape = Column(VARCHAR(25), nullable=False)
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)
    size = Column(Integer, nullable=False)
    drawing_id = Column(ForeignKey("drawings.id"))


Session = sessionmaker(bind=eng)
Base.metadata.create_all(eng)


def create_drawing(drawing_name, uid, pixel_data):
    sess = Session()
    drawing = Drawing(name=drawing_name, user=uid)

    for pixel in pixel_data:
        color = pixel.get("color")
        shape = pixel.get("shape")
        x = pixel.get("x")
        y = pixel.get("y")
        size = pixel.get("size")
        bp = BrushPixel(shape=shape, color=color, x=x, y=y, size=size)
        drawing.pixels.append(bp)

    sess.add(drawing)
    sess.commit()
    sess.close()

def save_drawing(drawing_name, uid, pixel_data_list):
    sess = Session()
    drawing = sess.query(Drawing).filter_by(name=drawing_name, user=uid).one_or_none()
    if not drawing:
        drawing = Drawing(name=drawing_name, user=uid)

    # TODO: This code exists because there is no proper cascade setup in the model.
    # It would be better if orphaning the old pixels automatically caused the system
    # to delete them.
    old_pixels = sess.query(BrushPixel).filter_by(drawing_id=drawing.id).all()
    for pixel in old_pixels:
        sess.delete(pixel)

    pixel_objects = []
    for pd in pixel_data_list:
        pixel = BrushPixel(color=pd.get("color"), shape=pd.get("shape"),
                           x=pd.get("x"), y=pd.get("y"), size=pd.get("size"))
        pixel_objects.append(pixel)

    drawing.pixels = pixel_objects
    sess.add(drawing)
    sess.commit()
    sess.close()

def create_user(uname, pw):
    sess = Session()
    hasher = hashlib.sha256()
    hasher.update(pw.encode())
    digest = hasher.hexdigest()
    user = User(username=uname, password=digest)
    sess.add(user)
    sess.commit()
    sess.close()
    return "created user: {}".format(uname)


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


def get_pixel_data(drawing_name, user_name):
    sess = Session()
    query = sess.query(Drawing).filter_by(name=drawing_name, user=user_name)
    drawing = query.one_or_none()
    if not drawing:
        return None
    else:
        pixels = drawing.pixels
        dict_list = [dict(color=p.color, shape=p.shape, x=p.x, y=p.y, size=p.size)
            for p in pixels]
        return dict_list


def is_password_valid(uname, pw, prehashed=False):
    if prehashed:
        password_arg = pw
    else:
        hasher = hashlib.sha256()
        hasher.update(pw.encode())
        password_arg = hasher.hexdigest()

    user = get_user(uname)
    if user and user.password == password_arg:
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