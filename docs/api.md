# Médecin API Documentation

This document provides an overview of the REST API endpoints available in the Médecin Hospital Management System.

## Base URL

```bash
http://127.0.0.1:8000/
```

## Endpoints

### Authentication

- **POST /auth/login/**: Authenticate a user and retrieve a token.
- **POST /auth/register/**: Register a new user.

### Patients

- **GET /patients/**: Retrieve a list of all patients.
- **POST /patients/**: Create a new patient record.
- **GET /patients/{id}/**: Retrieve details of a specific patient.
- **PUT /patients/{id}/**: Update a patient record.
- **DELETE /patients/{id}/**: Delete a patient record.

### Doctors

- **GET /doctors/**: Retrieve a list of all doctors.
- **POST /doctors/**: Add a new doctor.
- **GET /doctors/{id}/**: Retrieve details of a specific doctor.
- **PUT /doctors/{id}/**: Update a doctor's information.
- **DELETE /doctors/{id}/**: Remove a doctor from the system.

### Medical Records

- **GET /records/**: Retrieve a list of all medical records.
- **POST /records/**: Create a new medical record.
- **GET /records/{id}/**: Retrieve details of a specific medical record.
- **PUT /records/{id}/**: Update a medical record.
- **DELETE /records/{id}/**: Delete a medical record.

## Notes

- **Authentication**: All endpoints require a valid token except for the registration and login endpoints.
- **Data Formats**: Requests and responses use JSON format.

For more details, refer to the [project repository](https://github.com/okusjid/Medecin).
