# Médecin

Médecin is a simplified Hospital Management System built using Django. This system allows authenticated users to manage doctors, patients, and medical records efficiently. The project is designed to be modular, scalable, and easy to extend.

## Features

- **User Roles**:
  - **Admin**: Full control over managing doctors, patients, and medical records.
  - **Doctor**: Can view and manage their own patients and medical records.
  
- **Patient Management**:
  - Create, update, delete, and view patient information.
  - Search and filter patients easily.

- **Doctor Management**:
  - Manage doctors, including their specialization and contact information.
  - Search and filter doctors by specialization.

- **Medical Record Management**:
  - Create and manage medical records for patients.
  - View detailed information about each medical visit, including diagnosis and treatment.

- **Admin Site Customization**:
  - Django admin site customized for easy management of all entities.

## Technologies Used

- **Django**: A high-level Python web framework that encourages rapid development and clean, pragmatic design.
- **SQLite**: A lightweight, disk-based database that doesn’t require a separate server process.
- **HTML/CSS/JS**: For the front-end templates and static files.

## Installation

### Versions

- Python 3.12.4
- Django 5.1

### Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/medecin.git
   cd medecin
   ```

### Create a Virtual Environment (Optional but Recommended):
    ```bash
    python -m venv env
    source env/bin/activate  # On Windows: .\env\Scripts\activate
    ```
