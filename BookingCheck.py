import unittest
from datetime import datetime, date, time
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Time
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Define the database model
Base = declarative_base()

schedule_data = [
    {'date': '2022-12-10', 'start_time': time(7,00,00), 'end_time': time(9,00,00), 'price': 800000},
    {'date': '2022-12-10', 'start_time': time(9,00,00), 'end_time': time(11,00,00), 'price': 1000000},
    {'date': '2022-12-10', 'start_time': time(11,00,00), 'end_time': time(13,00,00), 'price': 1200000}
]

class Booking(Base):
    __tablename__ = 'booking'

    id = Column(Integer, primary_key=True)
    Booking_id = Column(String)
    venue_id = Column(Integer)
    User_id = Column(Integer)
    date = Column(DateTime)
    Start_time = Column(Time)
    end_time = Column(Time)
    price = Column(Integer)


# Create a test case class
class TestBookingSystem(unittest.TestCase):
    def setUp(self):
        engine = create_engine('sqlite:///:memory:')
        Session = sessionmaker(bind=engine)
        self.session = Session()

        Base.metadata.create_all(engine)

        # Insert sample data into the database
        self.session.add_all([
            Booking(id=1001, Booking_id='BK/000001', venue_id=15, User_id=12, date=date(2022,12,10), Start_time=time(9,00,00),
                    end_time=time(11,00,00), price=1200000),
            Booking(id=1005, Booking_id='BK/000005', venue_id=15, User_id=12, date=date(2022,12,10), Start_time=time(9,00,00),
                    end_time=time(11,00,00), price=1000000)
        ])

        self.session.commit()

    def test_incorrect_price(self):
        bookings = self.session.query(Booking).all()
        for booking in bookings:
            correct_price = self.get_correct_price(booking.date, booking.Start_time, booking.end_time)
            if booking.price != correct_price:
                print(f"Incorrect price for Booking ID: {booking.Booking_id}. Expected: {correct_price}, Actual: {booking.price}")

    def test_double_booking(self):
        bookings = self.session.query(Booking).all()
        for booking in bookings:
            conflicting_bookings = self.session.query(Booking).filter(
                Booking.venue_id == booking.venue_id,
                Booking.date == booking.date,
                Booking.Start_time == booking.Start_time,
                Booking.end_time == booking.end_time,
                Booking.id != booking.id
            ).all()
            if conflicting_bookings:
                print(f"Double booking detected for Booking ID: {booking.Booking_id}")
                #print("Conflicting bookings:")
                for conflicting_booking in conflicting_bookings:
                    print(conflicting_booking.Booking_id)

    def get_correct_price(self, date, start_time, end_time):
        for schedule in schedule_data:
            schedule_date = datetime.strptime(schedule['date'], '%Y-%m-%d').date()
            schedule_start_time = schedule['start_time']
            schedule_end_time = schedule['end_time']
            if schedule_date == date.date() and schedule_start_time == start_time and schedule_end_time == end_time:
                return schedule['price']
        return 0

if __name__ == '__main__':
    unittest.main()
