# Car Rental System - README

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [System Requirements](#system-requirements)
4. [Installation and Configuration](#installation-and-configuration)
5. [Operating the System](#operating-the-system)
6. [File Structure and Purpose](#file-structure-and-purpose)
7. [Licensing Terms](#licensing-terms)
8. [Known Issues](#known-issues)
9. [Credits](#credits)

---

## Introduction

The Car Rental System is a simple, user-friendly software designed to manage the operations of a car rental service. It allows users to register, view available cars, book cars, and manage car inventory. The system is built using Python and MySQL and follows a structured object-oriented approach.

This README provides step-by-step instructions on how to set up, install, and use the Car Rental System.

## Features

- **User Registration**: Customers and admins can register themselves in the system.
- **User Login**: Registered users can log in using their credentials.
- **Car Management**: Admins can add, update, and delete cars from the inventory.
- **Car Booking**: Customers can book available cars for specified periods.
- **Booking Management**: Admins can approve or cancel bookings.

## System Requirements

- **Operating System**: Any OS with Python support (Windows, macOS, Linux)
- **Python Version**: Python 3.7 or above
- **MySQL Database**: MySQL 5.7 or above
- **Required Libraries**:
  - `mysql-connector-python`: To connect Python with MySQL

## Installation and Configuration

### Step 1: Clone the Repository
First, clone the Car Rental System repository to your local machine:
```sh
git clone <repository-url>
```

### Step 2: Install Python Dependencies
Navigate to the project directory and install the required Python libraries:
```sh
pip install mysql-connector-python
```

### Step 3: Set Up MySQL Database

1. **Create Database**: Log in to your MySQL server using MySQL Workbench or the command line, and create a new database:
   ```sql
   CREATE DATABASE car_rental;
   ```

2. **Create Tables**: Execute the following SQL queries to create the necessary tables:

   - **Cars Table**:
     ```sql
     CREATE TABLE cars (
       car_id INT AUTO_INCREMENT PRIMARY KEY,
       make VARCHAR(50),
       model VARCHAR(50),
       year INT,
       mileage INT,
       available BOOLEAN,
       min_rent_period INT,
       max_rent_period INT
     );
     ```

   - **Users Table**:
     ```sql
     CREATE TABLE users (
       user_id INT AUTO_INCREMENT PRIMARY KEY,
       username VARCHAR(50) UNIQUE,
       password VARCHAR(50),
       role ENUM('customer', 'admin')
     );
     ```

   - **Bookings Table**:
     ```sql
     CREATE TABLE bookings (
       booking_id INT AUTO_INCREMENT PRIMARY KEY,
       user_id INT,
       car_id INT,
       start_date DATE,
       end_date DATE,
       rental_fee DECIMAL(10, 2),
       FOREIGN KEY (user_id) REFERENCES users(user_id),
       FOREIGN KEY (car_id) REFERENCES cars(car_id)
     );
     ```

3. **Add Sample Data**: Populate the `cars` table with sample data by executing the following SQL queries:
   ```sql
   INSERT INTO cars (make, model, year, mileage, available, min_rent_period, max_rent_period)
   VALUES ('Toyota', 'Corolla', 2018, 30000, TRUE, 1, 30),
          ('Honda', 'Civic', 2020, 15000, TRUE, 2, 15),
          -- Add 18 more records
          ('Ford', 'Fusion', 2019, 25000, TRUE, 3, 20);
   ```

### Step 4: Configure Database Connection

In the `CarDatabase` class in your Python code, update the following parameters to match your MySQL setup:

```python
self.conn = mysql.connector.connect(
    user='your_mysql_user',         # Replace with your MySQL username
    password='your_mysql_password', # Replace with your MySQL password
    host='localhost',               # Replace with your MySQL host
    database='car_rental'           # Replace with your MySQL database name
)
```

### Step 5: Run the Application

Now that everything is set up, you can run the `car_rental_system.py` file:

```sh
python car_rental_system.py
```

## Operating the System

- **Register a User**: The program allows both customers and admins to register using `register_user()` method.
- **Login**: Registered users can log in with their credentials using the `login_user()` method.
- **View Available Cars**: Customers can view available cars using the `view_available_cars()` method.
- **Book a Car**: Customers can book a car using the `book_car()` method.
- **Manage Cars**: Admins can add, update, and delete cars from the inventory using respective methods in the `CarDatabase` class.
- **Manage Bookings**: Admins can approve or cancel bookings using the `manage_bookings()` method.

## File Structure and Purpose

- **car_rental_system.py**: The main file containing all the classes and methods for the Car Rental System. This is the core of the application.
- **README.md**: This file, providing instructions on how to set up and use the Car Rental System.
- **requirements.txt**: Lists the Python packages required to run the system (e.g., `mysql-connector-python`).

## Licensing Terms

This project is licensed under the MIT License. You are free to use, modify, and distribute this software as long as the following conditions are met:

- **Attribution**: You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.
  
- **No Warranty**: This software is provided "as is", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and non-infringement. In no event shall the authors be liable for any claim, damages, or other liability, whether in an action of contract, tort, or otherwise, arising from, out of, or in connection with the software or the use or other dealings in the software.

For more details, please refer to the full [MIT License](https://opensource.org/licenses/MIT).

## Known Issues

- **Error Handling**: Error handling in the system is basic. Users should be cautious about entering correct data formats.
- **Scalability**: The current system is designed for small-scale use and may require optimization for larger datasets.

## Credits

This Car Rental System was developed by **Aman Jain** as a part of a software engineering project. For any queries or suggestions, please contact me at:

- **Email**: amanj120294@gmail.com
- **GitHub**: [https://github.com/AJ120294/CarRentalSystem.git](https://github.com/AJ120294/CarRentalSystem.git)

---

Thank you for using the Car Rental System!
