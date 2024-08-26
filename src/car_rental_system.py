import mysql.connector
from mysql.connector import errorcode

# User Class and its Subclasses: Customer and Admin

class User:
    def __init__(self, username, password, user_id=None):
        """
        Initialize a User object.

        :param username: The username of the user.
        :param password: The password of the user.
        :param user_id: The user's unique ID (auto-incremented by the database).
        """
        self.user_id = user_id  # user_id will be None initially, set after DB insertion
        self.username = username
        self.password = password

class Customer(User):
    def __init__(self, username, password, user_id=None):
        """
        Initialize a Customer object, inheriting from User.

        :param username: The username of the customer.
        :param password: The password of the customer.
        :param user_id: The customer's unique ID.
        """
        super().__init__(username, password, user_id)
        print(f"Customer '{username}' registered successfully with ID {self.user_id}.")

class Admin(User):
    def __init__(self, username, password, user_id=None):
        """
        Initialize an Admin object, inheriting from User.

        :param username: The username of the admin.
        :param password: The password of the admin.
        :param user_id: The admin's unique ID.
        """
        super().__init__(username, password, user_id)
        print(f"Admin '{username}' registered successfully with ID {self.user_id}.")

# UserFactory Class: Creates Users (Customers or Admins) Based on Role

class UserFactory:
    @staticmethod
    def create_user(role, username, password):
        """
        Factory method to create a User object based on the role.

        :param role: The role of the user ('customer' or 'admin').
        :param username: The username of the user.
        :param password: The password of the user.
        :return: A Customer or Admin object.
        """
        if role == "customer":
            return Customer(username, password)
        elif role == "admin":
            return Admin(username, password)
        else:
            raise ValueError("Invalid role")

# Car Class: Represents a Car Available for Rent

class Car:
    def __init__(self, make, model, year, mileage, available, min_rent_period, max_rent_period, car_id=None):
        """
        Initialize a Car object.

        :param make: The car's make (e.g., Toyota).
        :param model: The car's model (e.g., Corolla).
        :param year: The car's manufacturing year.
        :param mileage: The car's mileage.
        :param available: Boolean indicating if the car is available for rent.
        :param min_rent_period: The minimum rental period in days.
        :param max_rent_period: The maximum rental period in days.
        :param car_id: The car's unique ID (auto-incremented by the database).
        """
        self.car_id = car_id  # car_id will be None initially, set after DB insertion
        self.make = make
        self.model = model
        self.year = year
        self.mileage = mileage
        self.available = available
        self.min_rent_period = min_rent_period
        self.max_rent_period = max_rent_period
        print(f"Car '{self.make} {self.model}' added to the system.")

# CarDatabase Class: Manages Car Data in the Database (Singleton Pattern)

class CarDatabase:
    _instance = None

    def __new__(cls):
        """
        Ensures only one instance of CarDatabase exists (Singleton pattern).
        """
        if cls._instance is None:
            cls._instance = super(CarDatabase, cls).__new__(cls)
            cls._instance._connect_db()
        return cls._instance

    def _connect_db(self):
        """
        Connect to the MySQL database.
        """
        try:
            self.conn = mysql.connector.connect(
                user='root',  # replace with your MySQL username
                password='password',  # replace with your MySQL password
                host='localhost',  # replace with your MySQL host
                database='car_rental'  # replace with your MySQL database name
            )
            self.cursor = self.conn.cursor()
            print("Connected to the database successfully.")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your username or password.")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist.")
            else:
                print(err)

    def add_car(self, car):
        """
        Add a car to the database.

        :param car: The Car object to be added to the database.
        """
        add_car_query = (
            "INSERT INTO cars (make, model, year, mileage, available, min_rent_period, max_rent_period) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s)"
        )
        car_data = (car.make, car.model, car.year, car.mileage, car.available, car.min_rent_period, car.max_rent_period)
        self.cursor.execute(add_car_query, car_data)
        self.conn.commit()
        car.car_id = self.cursor.lastrowid  # Retrieve and set car_id after insertion
        print(f"Car '{car.make} {car.model}' added with ID: {car.car_id}.")

    def update_car(self, car_id, **kwargs):
        """
        Update a car's details in the database.

        :param car_id: The unique ID of the car to be updated.
        :param kwargs: Dictionary of attributes to update (e.g., make='Toyota').
        """
        update_query = "UPDATE cars SET "
        update_query += ", ".join(f"{key}=%s" for key in kwargs)
        update_query += " WHERE car_id=%s"
        update_data = list(kwargs.values()) + [car_id]
        self.cursor.execute(update_query, update_data)
        self.conn.commit()
        print(f"Car with ID {car_id} updated with values: {kwargs}.")

    def delete_car(self, car_id):
        """
        Delete a car from the database.

        :param car_id: The unique ID of the car to be deleted.
        """
        delete_query = "DELETE FROM cars WHERE car_id=%s"
        self.cursor.execute(delete_query, (car_id,))
        self.conn.commit()
        print(f"Car with ID {car_id} deleted.")

    def get_available_cars(self):
        """
        Retrieve all available cars from the database.

        :return: A list of Car objects representing available cars.
        """
        select_query = "SELECT * FROM cars WHERE available=TRUE"
        self.cursor.execute(select_query)
        result = self.cursor.fetchall()
        cars = []
        for row in result:
            car = Car(*row)
            cars.append(car)
        print(f"Retrieved {len(cars)} available cars from the database.")
        return cars

    def __del__(self):
        """
        Close the database connection when the CarDatabase object is destroyed.
        """
        self.cursor.close()
        self.conn.close()
        print("Database connection closed.")

# CarRentalSystem Class: Manages the Entire Car Rental Process

class CarRentalSystem:
    def __init__(self):
        """
        Initialize the CarRentalSystem, which handles users and car rentals.
        """
        self.users = {}  # Dictionary to store user objects
        self.car_database = CarDatabase()  # Single instance of the car database
        print("Car Rental System initialized.")

    def register_user(self, role, username, password):
        """
        Register a new user (either customer or admin).

        :param role: The role of the user ('customer' or 'admin').
        :param username: The username of the user.
        :param password: The password of the user.
        """
        user = UserFactory.create_user(role, username, password)
        self.users[username] = user
        print(f"User '{username}' registered as a {role}.")

    def login_user(self, username, password):
        """
        Log in a user and return the user object if credentials are correct.

        :param username: The username of the user.
        :param password: The password of the user.
        :return: The User object if login is successful, None otherwise.
        """
        user = self.users.get(username)
        if user and user.password == password:
            print(f"User '{username}' logged in successfully.")
            return user
        print(f"Login failed for user '{username}'.")
        return None

    def view_available_cars(self):
        """
        View a list of available cars.

        :return: A list of available Car objects.
        """
        cars = self.car_database.get_available_cars()
        print(f"Viewing available cars: {len(cars)} cars found.")
        return cars

    def book_car(self, username, car_id, start_date, end_date):
        """
        Book a car for a specified period.

        :param username: The username of the customer booking the car.
        :param car_id: The ID of the car to be booked.
        :param start_date: The start date of the booking.
        :param end_date: The end date of the booking.
        :return: The rental fee for the booking.
        """
        user = self.users.get(username)
        if not user:
            print(f"Booking failed: User '{username}' not found.")
            return None
        available_cars = self.view_available_cars()
        car = next((car for car in available_cars if car.car_id == car_id), None)
        if not car:
            print(f"Booking failed: Car with ID {car_id} is not available.")
            return None

        rental_duration = (end_date - start_date).days
        rental_fee = self.calculate_rental_fee(car, rental_duration)
        car.available = False  # Mark the car as unavailable

        # Assuming booking information is saved to a database, with booking_id auto-incremented
        booking_id = self.save_booking(user.user_id, car.car_id, start_date, end_date, rental_fee)
        print(f"Car booked successfully: Booking ID {booking_id}, Rental Fee: ${rental_fee:.2f}")
        return rental_fee

    def calculate_rental_fee(self, car, rental_duration):
        """
        Calculate the rental fee based on car and rental duration.

        :param car: The Car object being rented.
        :param rental_duration: The rental duration in days.
        :return: The total rental fee.
        """
        daily_rate = 50  # Example daily rate; this could vary by car
        total_fee = daily_rate * rental_duration
        print(f"Rental fee calculated: ${total_fee:.2f} for {rental_duration} days.")
        return total_fee

    def save_booking(self, user_id, car_id, start_date, end_date, rental_fee):
        """
        Save the booking to the database and return the booking ID.

        :param user_id: The ID of the user making the booking.
        :param car_id: The ID of the car being booked.
        :param start_date: The start date of the booking.
        :param end_date: The end date of the booking.
        :param rental_fee: The calculated rental fee.
        :return: The unique booking ID (auto-incremented by the database).
        """
        # Replace with actual database saving logic
        save_booking_query = (
            "INSERT INTO bookings (user_id, car_id, start_date, end_date, rental_fee) "
            "VALUES (%s, %s, %s, %s, %s)"
        )
        booking_data = (user_id, car_id, start_date, end_date, rental_fee)
        self.car_database.cursor.execute(save_booking_query, booking_data)
        self.car_database.conn.commit()
        booking_id = self.car_database.cursor.lastrowid  # Get the generated booking_id
        print(f"Booking saved with ID: {booking_id}.")
        return booking_id

    def manage_bookings(self, admin_username, booking_action, booking_id):
        """
        Manage bookings (only for admin users).

        :param admin_username: The username of the admin performing the action.
        :param booking_action: The action to perform ('approve', 'cancel', etc.).
        :param booking_id: The ID of the booking to be managed.
        """
        admin = self.users.get(admin_username)
        if not admin or not isinstance(admin, Admin):
            print(f"Action failed: '{admin_username}' is not an admin.")
            return

        # Example of managing a booking (actual logic will depend on requirements)
        if booking_action == "approve":
            print(f"Booking ID {booking_id} approved by admin {admin_username}.")
        elif booking_action == "cancel":
            print(f"Booking ID {booking_id} canceled by admin {admin_username}.")
        else:
            print(f"Unknown booking action: {booking_action}")