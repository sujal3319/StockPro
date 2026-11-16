# Stock Management System

A web-based inventory management application built with **Python Flask and MySQL**. The system enables efficient management of products, categories, suppliers, and stock levels through a centralized dashboard.

## Overview

The Stock Management System is designed to simplify inventory operations by providing a structured platform for maintaining product records, monitoring stock availability, and tracking inventory value.

## Key Features

- **Dashboard:** Overview of products, stock quantity, categories, suppliers, and inventory value.
- **Product Management:** Add, view, update, and delete product records.
- **Inventory Tracking:** Monitor available stock quantities.
- **Low Stock Alerts:** Identify products that require restocking.
- **Category Management:** Organize products into categories.
- **Supplier Management:** Maintain supplier information.
- **Product Search:** Quickly find products using search functionality.
- **Data Visualization:** View category-wise inventory statistics.

## Technology Stack

| Technology | Application |
|---|---|
| Python | Backend programming |
| Flask | Web application framework |
| MySQL | Relational database |
| HTML5 | Frontend structure |
| CSS3 | Styling |
| JavaScript | Client-side functionality |
| Bootstrap 5 | Responsive interface |
| Chart.js | Data visualization |

## Project Structure

```text
stock-management-system/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── templates/
│   ├── base.html
│   ├── index.html
│   └── products.html
│
└── static/
    ├── css/
    │   └── style.css
    └── js/
        ├── dashboard.js
        └── script.js
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/sujal3319/StockPro.git
```

### 2. Navigate to the project directory

```bash
cd stock-management-system
```

### 3. Create and activate a virtual environment

```bash
python -m venv venv
```

Windows:

```powershell
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure the database

Create a MySQL database named:

```sql
CREATE DATABASE stock_management;
```

Create the required tables using the database schema for this project. Configure your MySQL connection credentials through environment variables.

### 6. Run the application

```bash
python app.py
```

Open the following URL in your browser:

```text
http://127.0.0.1:5000/
```

## Configuration

The application requires the following environment variables:

| Variable | Description |
|---|---|
| `DB_HOST` | MySQL server hostname |
| `DB_USER` | MySQL username |
| `DB_PASSWORD` | MySQL password |
| `DB_NAME` | Database name |

Never commit database credentials or secret keys to the repository.

## Future Enhancements

- User authentication and role-based access control
- Sales and purchase management
- Invoice generation
- Excel and PDF report exports
- Advanced inventory analytics
- Cloud deployment

## Author

Developed as a database management and web development project using Python Flask and MySQL.

## License

This project is intended for educational and learning purposes.
