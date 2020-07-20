import random
import pandas as pd
from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Rectangle(Base):
    __tablename__ = 'rectangle'

    rectangle_id = Column(Integer, primary_key=True)
    a = Column(Integer, nullable=False)
    b = Column(Integer, nullable=False)
    area = Column(Integer, nullable=True)
    perimeter = Column(Integer, nullable=True)


class RectangleOperations:

    def __init__(self):
        self.engine = create_engine('sqlite:///rectangledb.db')

    def calc_area(self, a, b):
        return a * b

    def calc_perimeter(self, a, b):
        return (a + b) * 2

    def is_empty(self):
        """
        Check if there is a existing table.
        :return:
        Boolean: rectangle table existing or not.
        """
        if not self.engine.dialect.has_table(self.engine, 'Rectangle'):
            self.create_database_scheme()

        session = self.get_session()
        res = False if session.query(Rectangle).first() else True
        session.close()
        return res

    def get_session(self):
        return sessionmaker(bind=self.engine)()

    def create_database_scheme(self):
        Base.metadata.create_all(self.engine)

    def insert_test_data(self):
        """
        Create rectangle data for testing
        :return:
        """
        session = self.get_session()

        vals = []
        for i in range(20):
            a = random.randint(1, 100)
            b = random.randint(1, 100)
            rect = Rectangle(
                a=a,
                b=b,
            )
            vals.append(rect)

        session.add_all(vals)

        session.commit()
        session.close()

    def update_rectangle(self, rectangle_id):
        """
        Calculate perimeter and area of the rectangle by rectangle_id.
        :param
        rectangle_id (int):
        :return:
        2D-Lists: row of updated rectangle
        """
        session = self.get_session()

        rectangle = session.query(Rectangle).filter(
            Rectangle.rectangle_id == rectangle_id
        )

        rectangle_data = rectangle.one()

        a = rectangle_data.a
        b = rectangle_data.b

        area = self.calc_area(a, b)
        perimeter = self.calc_perimeter(a, b)

        vals = {
            'area': area,
            'perimeter': perimeter
        }
        rectangle.update(vals, synchronize_session='fetch')

        data = [[
            rectangle_data.rectangle_id,
            rectangle_data.a,
            rectangle_data.b,
            rectangle_data.area,
            rectangle_data.perimeter
        ]]

        session.commit()
        session.close()

        return data

    def show_rectangle_data(self, data=False):
        """
        Show all rectangle table or a row of rectangle
        :param
        data (2D-Lists): row of rectangle data
        """
        if not data:
            session = self.get_session()
            rectangles = session.query(Rectangle).all()

            data = [
                [rectangle.rectangle_id,
                 rectangle.a,
                 rectangle.b,
                 rectangle.area,
                 rectangle.perimeter]
                for rectangle in rectangles
            ]

            session.commit()
            session.close()

        data_frame = pd.DataFrame(
            data,
            columns=['rectangle_id', 'a', 'b', 'area', 'perimeter'],
            dtype=object
        )
        print(data_frame.to_string(index=False))
