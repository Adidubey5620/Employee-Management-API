# Employee Management API

A RESTful API for managing employee records built with FastAPI and Python.

## Features

- **Create Employees**: Add new employees with name, department, and salary information
- **Read Employees**: Retrieve all employees or fetch a specific employee by ID
- **Update Employees**: Fully update employee records or partially update specific fields
- **Delete Employees**: Remove employees from the system
- **Advanced Filtering**: Filter employees by department, salary range, or search by name
- **Sorting**: Sort employees by different fields in ascending or descending order
- **Pagination**: Navigate through large employee lists with configurable page size
- **Data Validation**: Comprehensive validation for all employee data

## Requirements

- Python 3.12 or higher
- FastAPI 0.139.2 or higher
- Uvicorn 0.51.0 or higher

## Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd Employee_Management_API
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment:**
   - On Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -e .
   ```

## Running the API

Start the development server:
```bash
python main.py
```

The API will be available at `http://127.0.0.1:8000`

Access the interactive API documentation at `http://127.0.0.1:8000/docs`

## API Endpoints

### Get All Employees
```
GET /employees
```

**Query Parameters:**
- `department` (optional): Filter by department name
- `min_salary` (optional): Filter by minimum salary
- `max_salary` (optional): Filter by maximum salary
- `search` (optional): Search by employee name
- `sort_by` (optional): Sort by field (e.g., name, salary)
- `order` (optional): Sort order - "asc" or "desc" (default: "asc")
- `page` (optional): Page number (default: 1)
- `limit` (optional): Records per page (default: 5)

**Example:**
```bash
curl "http://127.0.0.1:8000/employees?department=Engineering&min_salary=70000&page=1&limit=10"
```

### Get Employee by ID
```
GET /employees/{employee_id}
```

**Example:**
```bash
curl http://127.0.0.1:8000/employees/1
```

### Create Employee
```
POST /employees
```

**Request Body:**
```json
{
  "name": "John Doe",
  "department": "Engineering",
  "salary": 85000
}
```

**Example:**
```bash
curl -X POST http://127.0.0.1:8000/employees \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "department": "Engineering",
    "salary": 85000
  }'
```

### Update Employee (Full Update)
```
PUT /employees/{employee_id}
```

**Request Body:**
```json
{
  "name": "John Doe",
  "department": "Engineering",
  "salary": 90000
}
```

**Example:**
```bash
curl -X PUT http://127.0.0.1:8000/employees/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "department": "Engineering",
    "salary": 90000
  }'
```

### Partial Update Employee
```
PATCH /employees/{employee_id}
```

**Request Body (all fields optional):**
```json
{
  "salary": 95000
}
```

**Example:**
```bash
curl -X PATCH http://127.0.0.1:8000/employees/1 \
  -H "Content-Type: application/json" \
  -d '{
    "salary": 95000
  }'
```

### Delete Employee
```
DELETE /employees/{employee_id}
```

**Example:**
```bash
curl -X DELETE http://127.0.0.1:8000/employees/1
```

## Response Examples

### Success Response (Get Employee)
```json
{
  "id": 1,
  "name": "Alice",
  "department": "HR",
  "salary": 50000
}
```

### Error Response
```json
{
  "detail": "Employee not found"
}
```

## Error Handling

The API returns appropriate HTTP status codes:
- **200 OK**: Successful GET, PUT, PATCH, DELETE requests
- **201 Created**: Successful POST request
- **400 Bad Request**: Invalid input data or validation failure
- **404 Not Found**: Employee not found

## Data Validation

All employee data is validated:
- **Name**: Must not be empty
- **Department**: Must not be empty
- **Salary**: Must be greater than zero

## Project Structure

```
Employee_Management_API/
├── main.py                 # Application entry point
├── pyproject.toml         # Project dependencies and metadata
├── README.md              # This file
└── app/
    └── app.py             # FastAPI application and endpoints
```

## Development Notes

- The API currently uses in-memory storage (dictionary) for employee data
- Data is not persisted between server restarts
- For production use, consider implementing a database (e.g., PostgreSQL, MongoDB)

## License

This project is provided as-is for educational and development purposes.
