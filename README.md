# **Flask Hotel Booking App**

## **Overview**
The Flask Hotel Booking App is a web-based application designed to manage hotel bookings efficiently. It allows users to create, update, and cancel bookings while providing administrators with tools to manage customer data and pricing. The app is built using Flask, SQLAlchemy, and HTML/CSS for the frontend.

---

## **Features**

### **1. User Booking Management**
- **Create a Booking**:
  - Users can select a room type, meal deal, and specify the number of nights and people.
  - The app calculates the total price based on the selected options and any applicable deals.
- **Update a Booking**:
  - Users can modify their booking details, including check-in and check-out dates, number of people, and meal deals.
  - The app recalculates the total price dynamically based on the updated details.
- **Cancel a Booking**:
  - Users can cancel their booking, which removes the booking and associated customer data from the database.

---

### **2. Login and Authentication**
- **Booking Login**:
  - Users can log in using their booking number and surname to manage their bookings.
  - The app validates the credentials against the database to ensure secure access.

---

### **3. Pricing and Deals**
- **Dynamic Pricing**:
  - The app calculates the total price based on room type, meal deal, and the number of nights.
- **Special Deals**:
  - Discounts are applied automatically for eligible bookings (e.g., weekly deals for 7-night stays).
  - The app ensures that deals are applied only when conditions are met.

---

### **4. Session Management**
- **Persistent User Data**:
  - The app uses Flask sessions to store user data (e.g., booking number, surname) securely during their session.
- **Session Expiry**:
  - Sessions are managed securely with a secret key to prevent unauthorized access.

---

### **5. Database Integration**
- **SQLAlchemy ORM**:
  - The app uses SQLAlchemy to interact with the database, ensuring efficient and secure data handling.
- **CRUD Operations**:
  - Supports Create, Read, Update, and Delete operations for bookings and customer data.

---

### **6. Error Handling and Validation**
- **Form Validation**:
  - Ensures all required fields are filled before processing a booking or update.
- **Error Messages**:
  - Displays user-friendly error messages for invalid inputs or missing data.
- **Debugging Tools**:
  - Includes debug statements to log key variables and flow control for easier troubleshooting.

---

### **7. Responsive Frontend**
- **HTML/CSS Templates**:
  - The app uses Flask's Jinja2 templating engine to render dynamic HTML pages.
- **User-Friendly Interface**:
  - Clean and intuitive design for managing bookings.

---

### **8. Admin Features (Optional)**
- **Customer Management**:
  - Administrators can view and manage customer data.
- **Booking Insights**:
  - Provides insights into bookings, such as total revenue and popular room types.

---

## **Technologies Used**
- **Backend**: Flask (Python), SQLAlchemy
- **Frontend**: HTML, CSS, Jinja2, Bootstrap
- **Database**: SQLite (or any SQLAlchemy-supported database)
- **Session Management**: Flask Sessions

---

## **How to Run the App**
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Flask-Hotel-Booking-App
2. Install dependencies:
   pip install -r requirements.txt
4. Run the Flask app:
   python run app.py
