from flask import Flask, render_template, request, redirect, url_for, session, flash
from random import randint
from datetime import *
import sqlalchemy as sa
from sqlalchemy import ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker, declarative_base

app = Flask(__name__) # <-- to set up our flask application while refencing this file
sqlite_file_name = "instance/Flora_Hotel.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
db = sa.create_engine(sqlite_url) # <-- this initializes our database
Session = sessionmaker(bind=db)
app.secret_key = "41038"  # <-- secret key for session management
Base = declarative_base()


# Creating the models of our database
# model = table

class Booking(Base):
    __tablename__ = "booking"

    booking_number: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        default=lambda: randint(100000, 999999)  # setting a default value automatically
    )
    check_in: Mapped[date]
    check_out: Mapped[date]
    room_selection: Mapped[str] = mapped_column(ForeignKey("rooms.room_name"))
    nights: Mapped[int]
    people: Mapped[int]
    total_price: Mapped[int]
    location: Mapped[str]
    meal_deal: Mapped[str]

    def __repr__(self):
        return f"<Booking(booking_number={self.booking_number}, check_in={self.check_in}, check_out={self.check_out}, room_selection={self.room_selection}, nights={self.nights}, people={self.people}, total_price={self.total_price}, location={self.location}, meal_deal={self.meal_deal})>"


class Customer(Base):
    __tablename__ = "customers"
    booking_number: Mapped[int] = mapped_column(Integer, ForeignKey("booking.booking_number"), primary_key=True,
                                                default="booking.booking_number")
    name: Mapped[str]
    surname: Mapped[str]
    email: Mapped[str]
    address: Mapped[str]
    telephone: Mapped[int]

    def __repr__(self):
        return f"<Customer(booking_number={self.booking_number}, name={self.name}, surname={self.surname}, email={self.email}, address={self.address}, telephone={self.telephone})>"

class MealDeals(Base):
    __tablename__ = "meal_deals"

    meal_deal_name: Mapped[str] = mapped_column(primary_key=True)
    meal_deal_price: Mapped[int]

    def __repr__(self):
        return f"<MealDeals(meal_deal_name={self.meal_deal_name}, meal_deal_price={self.meal_deal_price})>"

class Rooms(Base):
    __tablename__ = "rooms"

    room_name: Mapped[str] = mapped_column(primary_key=True)
    price_per_night: Mapped[int]
    size: Mapped[str]
    bed: Mapped[str]
    image_file_name: Mapped[str]
    location: Mapped[str]
    description_pitch: Mapped[str]

    def __repr__(self):
        return f"<Rooms(room_name={self.room_name}, price_per_night={self.price_per_night}, size={self.size}, image_path={self.image_file_name}, location={self.location}, description={self.description_pitch})>"

class Deals(Base):
    __tablename__ = "deals"

    deal_name: Mapped[str] = mapped_column(primary_key=True)
    room_location: Mapped[str]
    room_name: Mapped[str]
    nights: Mapped[str]
    new_price: Mapped[int]
    old_price: Mapped[int]

    def __repr__(self):
        return f"Deals(deal_name={self.deal_name}, room_location={self.room_location}, room_name={self.room_name}, new_price={self.new_price}, old_price={self.old_price})"

#Base.metadata.drop_all(db)
#Base.metadata.create_all(db) # <-- makes the actual tables with headers(columns) in the database

# creating objects representing rows that should be already in the database
# the program will be collecting data from them
meal_deal_1 = MealDeals(meal_deal_name="Bed & Breakfast", meal_deal_price=5)
meal_deal_2 = MealDeals(meal_deal_name="All Inclusive", meal_deal_price=10)
meal_deals = [meal_deal_1, meal_deal_2]

room_1 = Rooms(room_name="Standard Room", price_per_night=15, size="20-30 sqm", bed="single sized bed", image_file_name="standard hotel room.png", location="United Kingdom", description_pitch="quick refreshing stay")
room_2 = Rooms(room_name="Premium Room", price_per_night=18, size="25-35 sqm", bed="double sized bed", image_file_name="premium room.png", location="United Kingdom", description_pitch="higher quality stay within the budget")
room_3 = Rooms(room_name="Exclusive Room", price_per_night=25, size="30-40 sqm", bed="queen sized bed", image_file_name="exclusive hotel room.jpg", location="United Kingdom", description_pitch="exclusive above the standard experience")
room_4 = Rooms(room_name="Deluxe Room", price_per_night=30, size="35-45 sqm", bed="king sized bed", image_file_name="deluxe room.jpg", location="United Kingdom", description_pitch="top-notch luxurious stay")
rooms = [room_1, room_2, room_3, room_4]


deal_1 = Deals(deal_name="Premium Bundle", room_location="London, UK", room_name="Premium Room", nights="7 nights", new_price=100, old_price=126)
deal_2 = Deals(deal_name="Exclusive Bundle", room_location="London, UK", room_name="Exclusive Room", nights="7 nights", new_price=150, old_price=175)
deal_3 = Deals(deal_name="Deluxe Bundle", room_location="London, UK", room_name="Deluxe Room", nights="7 nights", new_price=170, old_price=210)
deals = [deal_1, deal_2, deal_3]


def commit_to_database(object):
    with Session() as session:
        session.add(object)
        session.commit()
        session.refresh(object)  # <-- refresh the object to get the updated state from the database
        print(f"Object {object} committed to the database.")

"""
for deal in meal_deals:
    commit_to_database(deal)

for room in rooms:
    commit_to_database(room)

for deal in deals:
    commit_to_database(deal)
"""
# Finally, I'll begin to construct the web application

@app.route("/", methods=["GET", "POST"]) # <-- default page, no request needed = path left empty + GET and POST request method used
def homepage():
    if request.method == "POST":
        print("POST request received")
        location = request.form["location"]
        check_in = request.form["check_in"]
        check_out = request.form["check_out"]
        people = request.form["people"]
        print(location, check_in, check_out, people)
        if location and check_in and check_out and people:
            # Convert check_in and check_out to datetime.date objects
            check_in_date = datetime.strptime(check_in, "%Y-%m-%d").date()
            check_out_date = datetime.strptime(check_out, "%Y-%m-%d").date()
            nights = (check_out_date - check_in_date).days
            print(nights)
            session["nights"] = nights
            session["location"] = location
            session["check_in"] = check_in_date
            session["check_out"] = check_out_date
            session["people"] = int(people)
            return redirect(url_for('search_results'))
        else:
            flash("All fields are required", "info")
            return render_template("Home.html")
    else:
        print("GET request received")
        return render_template("Home.html")

@app.route("/about", methods=["GET", "POST"])
def about():
    return render_template("About Us.html")

@app.route("/search_results", methods=["GET", "POST"])
def search_results():
    if "location" in session:
        location = session["location"]
        with Session() as db_session:
            rooms = db_session.query(Rooms).filter(Rooms.location == location).all()
        return render_template("Search Results.html", location=location, rooms=rooms)
    else:
        return redirect(url_for("homepage"))


@app.route("/Deals")
def room_deals():
    with Session() as db_session:
        deals = db_session.query(Deals).all()
        rooms = db_session.query(Rooms).all()
    return render_template("Deals.html", deals=deals, rooms=rooms)


# function that will be used to create a booking object and commit it to the database
def create_booking(room, meal_deal, nights, people, location, check_in, check_out, room_deal):
    total_price = room_deal_condition(room, nights, meal_deal, room_deal)
    check_in_date = datetime.strptime(check_in, "%a, %d %b %Y %H:%M:%S %Z").date()
    check_out_date= datetime.strptime(check_out, "%a, %d %b %Y %H:%M:%S %Z").date()
    booking = Booking(
        check_in=check_in_date,
        check_out=check_out_date,
        room_selection=room.room_name,
        nights=nights,
        people=people,
        total_price=total_price,
        location=location,
        meal_deal=meal_deal.meal_deal_name
    )
    try:
        commit_to_database(booking)
        print("Booking created")
    except Exception as e:
        print(f"Failed to create booking: {e}")
        raise
    return booking

def room_deal_condition(room, nights, meal_deal, room_deal):
    if nights != 7 or room.room_name == "Standard Room":
        total_price = meal_deal.meal_deal_price * nights + room.price_per_night * nights
        return total_price 
    else:
        total_price = meal_deal.meal_deal_price * nights + room_deal.new_price
        return total_price

@app.route("/Standard Room", methods=["GET", "POST"])
def standard_room():
    location = session["location"]
    nights = session["nights"]
    people = session["people"]
    check_in = session["check_in"]
    check_out = session["check_out"]    
    with Session() as db_session:
        room = db_session.query(Rooms).filter(Rooms.room_name == "Standard Room", Rooms.location == location).first()
        meal_deal = db_session.query(MealDeals).filter(MealDeals.meal_deal_name == "Bed & Breakfast").first()
        room_deal = None # <-- this is the standard meal deal
        if request.method == "POST":
            if "B&b" in request.form:
                meal_deal = db_session.query(MealDeals).filter(MealDeals.meal_deal_name == "Bed & Breakfast").first() # <-- this is the standard meal deal
                print("B&b selected")
                if 'book' in request.form:
                    print("Book button clicked")
                    user_booking = create_booking(room, meal_deal, nights, people, location, check_in, check_out, room_deal)
                    session['booking_number'] = user_booking.booking_number
                    print("Booking number:", user_booking.booking_number)
                    return redirect(url_for("booking_confirmation"))
                else:
                    return render_template("Standard Room.html", room=room, meal_deal=meal_deal, location=location, nights=nights, people=people)
            elif "all_inclusive" in request.form:
                meal_deal = db_session.query(MealDeals).filter(MealDeals.meal_deal_name == "All Inclusive").first()
                print("All Inclusive selected")
                if 'book' in request.form:
                    print("Book button clicked")
                    user_booking = create_booking(room, meal_deal, nights, people, location, check_in, check_out, room_deal)
                    session['booking_number'] = user_booking.booking_number
                    print("Booking number:", user_booking.booking_number)
                    return redirect(url_for("booking_confirmation"))
                else:
                    return render_template("Standard Room.html", room=room, meal_deal=meal_deal, location=location, nights=nights, people=people)
            else:
                if 'book' in request.form:
                    print("Book button clicked")
                    user_booking = create_booking(room, meal_deal, nights, people, location, check_in, check_out, room_deal)
                    session['booking_number'] = user_booking.booking_number
                    print("Booking number:", user_booking.booking_number)
                    return redirect(url_for("booking_confirmation"))
                else:
                    return render_template("Standard Room.html", room=room, meal_deal=meal_deal, location=location, nights=nights, people=people)
    
    return render_template("Standard Room.html", room=room, meal_deal=meal_deal, location=location, nights=nights, people=people)
        

@app.route("/Premium Room", methods=["GET", "POST"])
def premium_room():
    location = session["location"]
    nights = session["nights"]
    people = session["people"]
    with Session() as db_session:
        room = db_session.query(Rooms).filter(Rooms.room_name == "Premium Room", Rooms.location == location).first()
        check_in = session["check_in"]
        check_out = session["check_out"]
        meal_deal = db_session.query(MealDeals).filter(MealDeals.meal_deal_name == "Bed & Breakfast").first()
        room_deal = db_session.query(Deals).filter(Deals.room_name == "Premium Room").first()
        if request.method == "POST":
            if "B&b" in request.form:
                meal_deal = db_session.query(MealDeals).filter(MealDeals.meal_deal_name == "Bed & Breakfast").first() # <-- this is the standard meal deal
                print("B&b selected")
                if 'book' in request.form:
                    print("Book button clicked")
                    user_booking = create_booking(room, meal_deal, nights, people, location, check_in, check_out, room_deal)
                    session['booking_number'] = user_booking.booking_number
                    print("Booking number:", user_booking.booking_number)
                    return redirect(url_for("booking_confirmation"))
                else:
                    return render_template("Premium Room.html", room=room, meal_deal=meal_deal, location=location, nights=nights, people=people, room_deal=room_deal)
            elif "all_inclusive" in request.form:
                meal_deal = db_session.query(MealDeals).filter(MealDeals.meal_deal_name == "All Inclusive").first()
                print("All Inclusive selected")
                if 'book' in request.form:
                    print("Book button clicked")
                    user_booking = create_booking(room, meal_deal, nights, people, location, check_in, check_out, room_deal)
                    session['booking_number'] = user_booking.booking_number
                    print("Booking number:", user_booking.booking_number)
                    return redirect(url_for("booking_confirmation"))
                else:
                    return render_template("Premium Room.html", room=room, meal_deal=meal_deal, location=location, nights=nights, people=people, room_deal=room_deal)
            else:
                if 'book' in request.form:
                    print("Book button clicked")
                    user_booking = create_booking(room, meal_deal, nights, people, location, check_in, check_out, room_deal)
                    session['booking_number'] = user_booking.booking_number
                    print("Booking number:", user_booking.booking_number)
                    return redirect(url_for("booking_confirmation"))
                else:
                    return render_template("Premium Room.html", room=room, meal_deal=meal_deal, location=location, nights=nights, people=people)
    
    return render_template("Premium Room.html", room=room, meal_deal=meal_deal, location=location, nights=nights, people=people, room_deal=room_deal)



@app.route("/Exclusive Room", methods=["GET", "POST"])
def exclusive_room():
    location = session["location"]
    nights = session["nights"]
    people = session["people"]
    check_in = session["check_in"]
    check_out = session["check_out"]    
    with Session() as db_session:
        room = db_session.query(Rooms).filter(Rooms.room_name == "Exclusive Room", Rooms.location == location).first()
        meal_deal = db_session.query(MealDeals).filter(MealDeals.meal_deal_name == "Bed & Breakfast").first()
        room_deal = db_session.query(Deals).filter(Deals.room_name == "Exclusive Room").first()
        if request.method == "POST":
            if "B&b" in request.form:
                meal_deal = db_session.query(MealDeals).filter(MealDeals.meal_deal_name == "Bed & Breakfast").first() # <-- this is the standard meal deal
                print("B&b selected")
                if 'book' in request.form:
                    print("Book button clicked")
                    user_booking = create_booking(room, meal_deal, nights, people, location, check_in, check_out, room_deal)
                    session['booking_number'] = user_booking.booking_number
                    print("Booking number:", user_booking.booking_number)
                    return redirect(url_for("booking_confirmation"))
                else:
                    return render_template("Exclusive Room.html", room=room, meal_deal=meal_deal, location=location, nights=nights, people=people, room_deal=room_deal)
            elif "all_inclusive" in request.form:
                meal_deal = db_session.query(MealDeals).filter(MealDeals.meal_deal_name == "All Inclusive").first()
                print("All Inclusive selected")
                if 'book' in request.form:
                    print("Book button clicked")
                    user_booking = create_booking(room, meal_deal, nights, people, location, check_in, check_out, room_deal)
                    session['booking_number'] = user_booking.booking_number
                    print("Booking number:", user_booking.booking_number)
                    return redirect(url_for("booking_confirmation"))
                else:
                    return render_template("Exclusive Room.html", room=room, meal_deal=meal_deal, location=location, nights=nights, people=people, room_deal=room_deal)
            else:
                if 'book' in request.form:
                    print("Book button clicked")
                    user_booking = create_booking(room, meal_deal, nights, people, location, check_in, check_out, room_deal)
                    session['booking_number'] = user_booking.booking_number
                    print("Booking number:", user_booking.booking_number)
                    return redirect(url_for("booking_confirmation"))
                else:
                    return render_template("Standard Room.html", room=room, meal_deal=meal_deal, location=location, nights=nights, people=people, room_deal=room_deal)
    
    return render_template("Exclusive Room.html", room=room, meal_deal=meal_deal, location=location, nights=nights, people=people, room_deal=room_deal)


@app.route("/Deluxe Room", methods=["GET", "POST"])
def deluxe_room():
    location = session["location"]
    nights = session["nights"]
    people = session["people"]
    check_in = session["check_in"]
    check_out = session["check_out"]    
    with Session() as db_session:
        room = db_session.query(Rooms).filter(Rooms.room_name == "Deluxe Room", Rooms.location == location).first()
        meal_deal = db_session.query(MealDeals).filter(MealDeals.meal_deal_name == "Bed & Breakfast").first()
        room_deal = db_session.query(Deals).filter(Deals.room_name == "Deluxe Room").first()
        if request.method == "POST":
            if "B&b" in request.form:
                meal_deal = db_session.query(MealDeals).filter(MealDeals.meal_deal_name == "Bed & Breakfast").first() # <-- this is the standard meal deal
                print("B&b selected")
                if 'book' in request.form:
                    print("Book button clicked")
                    user_booking = create_booking(room, meal_deal, nights, people, location, check_in, check_out, room_deal)
                    session['booking_number'] = user_booking.booking_number
                    print("Booking number:", user_booking.booking_number)
                    return redirect(url_for("booking_confirmation"))
                else:
                    return render_template("Deluxe Room.html", room=room, meal_deal=meal_deal, location=location, nights=nights, people=people)
            elif "all_inclusive" in request.form:
                meal_deal = db_session.query(MealDeals).filter(MealDeals.meal_deal_name == "All Inclusive").first()
                print("All Inclusive selected")
                if 'book' in request.form:
                    print("Book button clicked")
                    user_booking = create_booking(room, meal_deal, nights, people, location, check_in, check_out, room_deal)
                    session['booking_number'] = user_booking.booking_number
                    print("Booking number:", user_booking.booking_number)
                    return redirect(url_for("booking_confirmation"))
                else:
                    return render_template("Deluxe Room.html", room=room, meal_deal=meal_deal, location=location, nights=nights, people=people, room_deal=room_deal)
            else:
                if 'book' in request.form:
                    print("Book button clicked")
                    user_booking = create_booking(room, meal_deal, nights, people, location, check_in, check_out, room_deal)
                    session['booking_number'] = user_booking.booking_number
                    print("Booking number:", user_booking.booking_number)
                    return redirect(url_for("booking_confirmation"))
                else:
                    return render_template("Deluxe Room.html", room=room, meal_deal=meal_deal, location=location, nights=nights, people=people, room_deal=room_deal)
    
    return render_template("Deluxe Room.html", room=room, meal_deal=meal_deal, location=location, nights=nights, people=people, room_deal=room_deal)

@app.route("/Booking Confirmation")
def booking_confirmation():
    user_booking_number = session["booking_number"]
    with Session() as db_session:
        booking = db_session.query(Booking).filter(Booking.booking_number == user_booking_number).first()
    if booking:
        return redirect(url_for("details"))
    return render_template("Confirm Booking.html", booking=booking)

@app.route("/Details", methods=["GET", "POST"])
def details():
    if request.method == "POST":
        full_name = request.form["name"]
        email = request.form["email"]
        address = request.form["address"]
        telephone = request.form["number"]
        booking_number = session["booking_number"]
        if full_name and email and address and telephone:
            print("All fields are filled")
            customer = Customer(
                booking_number=booking_number,
                name=full_name.split()[0],  # Assuming the first part is the name
                surname=full_name.split()[1],  # Assuming the second part is the surname
                email=email,
                address=address,
                telephone=telephone
            )
            session['surname'] = full_name.split()[1]
            commit_to_database(customer)
            print(f"{full_name} was added to the database")
            return redirect(url_for("successful_booking"))
        else:
            flash("All fields are required", "info")
            return render_template("Enter Details.html")
    else:
        return render_template("Enter Details.html")


@app.route("/successful_booking")
def successful_booking():
    user_booking_number = session["booking_number"]
    with Session() as db_session:
        booking = db_session.query(Booking).filter(Booking.booking_number == user_booking_number).first()
        customer = db_session.query(Customer).filter(Customer.booking_number == user_booking_number).first()
    return render_template("Booking Successful.html", booking=booking, customer=customer)

@app.route("/login_booking", methods=["GET", "POST"])
def login_booking():
    
    if request.method == "POST":
        user_booking_number = request.form["booking_number"]
        user_surname = request.form["surname"]

        with Session() as db_session:
            customer = db_session.query(Customer).filter(
                Customer.booking_number == user_booking_number,
                Customer.surname == user_surname
            ).first()
    
            if customer:
                booking = db_session.query(Booking).filter(Booking.booking_number == user_booking_number).first()
                session["booking_number"] = user_booking_number
                session["surname"] = user_surname
                print(f"User {user_surname} logged in successfully")
                return redirect(url_for("manage_booking"))
            else:
                flash("Incorrect booking number or surname", "info")
                return render_template("Manage Booking Login.html")
            
    else:        
        return render_template("Manage Booking Login.html")

@app.route("/manage_booking", methods=["GET", "POST"])
def manage_booking():
    booking_number = session["booking_number"]
    with Session() as db_session:
        booking = db_session.query(Booking).filter(Booking.booking_number == booking_number).first()
        customer = db_session.query(Customer).filter(Customer.booking_number == booking_number).first()
    if request.method == "POST":
        if "cancel" in request.form:
            print("User wants to cancel the booking")
            return redirect(url_for("cancel_booking_warning"))
        elif "change" in request.form:
            return redirect(url_for("change_booking"))
    else:
        return render_template("Manage Booking.html", booking=booking, customer=customer)

@app.route("/cancel_booking_warning", methods=["GET", "POST"])
def cancel_booking_warning():
    booking_number = session["booking_number"]
    with Session() as db_session:
        booking = db_session.query(Booking).filter(Booking.booking_number == booking_number).first()
        customer = db_session.query(Customer).filter(Customer.booking_number == booking_number).first()
    if request.method == "POST":
        if "Yes" in request.form:
            print("User wants to cancel the booking pt. 2")
            return redirect(url_for("cancel_booking"))
        elif  "No" in request.form:
            print("User wants to keep the booking")
            return redirect(url_for("manage_booking"))
    else:
        return render_template("Cancel Warning.html", booking=booking, customer=customer)

@app.route("/cancel_booking", methods=["GET", "POST"])
def cancel_booking():
    booking_number = session["booking_number"]
    with Session() as db_session:
        booking = db_session.query(Booking).filter(Booking.booking_number == booking_number).first()
        customer = db_session.query(Customer).filter(Customer.booking_number == booking_number).first()
        db_session.delete(booking)
        db_session.delete(customer)
        db_session.commit()
        print(f"Booking {booking_number} and customer {customer.name} were deleted from the database")
    return render_template("Booking Cancelled.html", booking=booking, customer=customer)

@app.route("/change_booking", methods=["GET", "POST"])
def change_booking():
    booking_number = session["booking_number"]
    with Session() as db_session:
        booking = db_session.query(Booking).filter(Booking.booking_number == booking_number).first()
        customer = db_session.query(Customer).filter(Customer.booking_number == booking_number).first()
        if request.method == "POST":
            if "check_in" not in request.form or "check_out"  not in request.form:
                return "Error: Required fields are missing in the form submission", 400
            
            new_check_in = request.form["check_in"]
            new_check_out = request.form["check_out"]
            new_people = request.form["people"]
            new_meal_deal = request.form["meal_deal"]
            check_in_date = datetime.strptime(new_check_in, "%Y-%m-%d").date()
            check_out_date = datetime.strptime(new_check_out, "%Y-%m-%d").date()
            nights = (check_out_date - check_in_date).days
            session["new_check_in"] = check_in_date
            session["new_check_out"] = check_out_date
            session["new_people"] = new_people
            session["new_nights"] = nights
            session["new_meal_deal"] = new_meal_deal
            return redirect(url_for("change_booking_confirmation"))
        else:    
            return render_template("Change Booking.html", booking=booking, customer=customer)

@app.route("/change_booking_confirmation", methods=["GET", "POST"])
def change_booking_confirmation():
    check_in_date = session["new_check_in"] 
    new_check_out = session["new_check_out"] 
    new_people = session["new_people"]
    new_nights = session["new_nights"] 
    new_meal_deal = session["new_meal_deal"]
    booking_number = session["booking_number"]
    print(check_in_date, new_check_out, new_people, new_nights, new_meal_deal)
    new_check_in =  datetime.strptime(session["new_check_in"], "%a, %d %b %Y %H:%M:%S %Z").date()
    with Session() as db_session:
        booking = db_session.query(Booking).filter(Booking.booking_number == booking_number).first()
        customer = db_session.query(Customer).filter(Customer.booking_number == booking_number).first()
        old_check_in = booking.check_in

        if request.method == "POST": 
            if "confirm" in request.form:
                print("User confirmed the booking change.")  
                check_in_date = new_check_in #<-- already in the correct format
                check_out_date = datetime.strptime(new_check_out, "%a, %d %b %Y %H:%M:%S %Z").date()

                # Update booking object
                booking.check_in = check_in_date
                booking.check_out = check_out_date
                booking.nights = new_nights
                booking.people = new_people
                booking.meal_deal = new_meal_deal 
                db_session.commit()
                print("Booking updated in the database.")  # Debugging

                
                room = db_session.query(Rooms).filter(Rooms.room_name == booking.room_selection).first()
                meal_deal = db_session.query(MealDeals).filter(MealDeals.meal_deal_name == new_meal_deal).first()
                room_deal = db_session.query(Deals).filter(Deals.room_name == booking.room_selection).first()

                # Update the total price based on the new values
                booking.total_price = room_deal_condition(room, new_nights, meal_deal, room_deal)
                db_session.commit()

                print("Booking updated")
                return redirect(url_for("change_booking_successful"))
            elif "deny" in request.form:
                print("User wants to keep the booking")
                return redirect(url_for("change_booking"))
        else: 
            return render_template("Change Confirm.html", booking=booking, customer=customer, old_check_in=old_check_in, new_check_in=new_check_in)
    
@app.route("/change_booking_successful")
def change_booking_successful():
    booking_number = session["booking_number"]
    with Session() as db_session:
        booking = db_session.query(Booking).filter(Booking.booking_number == booking_number).first()
        customer = db_session.query(Customer).filter(Customer.booking_number == booking_number).first()
    return render_template("Booking Change Successful.html", booking=booking, customer=customer)



if __name__ == "__main__":
    app.run(debug=True)