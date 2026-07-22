from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI(
    title="Employee Management API",
    version="1.0"
)

class EmployeeResponse(BaseModel):
    id: int
    name: str
    department: str
    salary: int


class EmployeeCreate(BaseModel):
    name: str = Field(..., min_length=1)
    department: str = Field(..., min_length=1)
    salary: int = Field(..., gt=0)

class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    department: Optional[str] = None
    salary: Optional[int] = None


employees = {
    1: {
        "name": "Alice",
        "department": "HR",
        "salary": 50000
    },
    2: {
        "name": "Bob",
        "department": "Engineering",
        "salary": 80000
    },
    3: {
        "name": "Charlie",
        "department": "Marketing",
        "salary": 60000
    }
}


# @app.get(
#     "/employees",
#     response_model=list[EmployeeResponse]
# )
# def get_all_employees():

#     result = []

#     for employee_id, employee in employees.items():

#         result.append(
#             {
#                 "id": employee_id,
#                 **employee
#             }
#         )

#     return result


def validate_employee(name: str, department: str, salary: int):

    if not name.strip():
        raise HTTPException(
            status_code=400,
            detail="Employee name cannot be empty"
        )

    if not department.strip():
        raise HTTPException(
            status_code=400,    
            detail="Department cannot be empty"
        )

    if salary <= 0:
        raise HTTPException(
            status_code=400,
            detail="Salary must be greater than zero"
        )

@app.get(
    "/employees/{employee_id}",
    response_model=EmployeeResponse,
    status_code=200
)
def get_employee(employee_id: int):

    if employee_id not in employees:

        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return {
        "id": employee_id,
        **employees[employee_id]
    }

@app.post(
    "/employees",
    response_model=EmployeeResponse,
    status_code=201
)
def create_employee(employee: EmployeeCreate):

    validate_employee(
        employee.name,
        employee.department,
        employee.salary
    )

    new_id = max(employees.keys()) + 1

    employees[new_id] = {
        "name": employee.name,
        "department": employee.department,
        "salary": employee.salary
    }

    return {
        "id": new_id,
        **employees[new_id]
    }

@app.put(
    "/employees/{employee_id}",
    response_model=EmployeeResponse,
    status_code=200
    )
def update_employee(employee_id: int, employee: EmployeeCreate):

    if employee_id not in employees:
        raise HTTPException(
            status_code=400,
            detail="Employee not found"
        )
    
    validate_employee(
        employee.name,
        employee.department,
        employee.salary
    )
    
    employees[employee_id] = {
    "name": employee.name,
    "department": employee.department,
    "salary": employee.salary
    }
    return {
        "id": employee_id,
        **employees[employee_id]
    }
    

@app.patch(
    "/employees/{employee_id}",
    response_model=EmployeeResponse,
    status_code=200
    )
def patch_employee(
    employee_id: int,
    employee: EmployeeUpdate
):
    if employee_id not in employees:
        raise HTTPException(
            status_code=400,
            detail="Employee not found"
        )
    
    if (
        employee.name is None and
        employee.department is None and
        employee.salary is None
    ):
        raise HTTPException(
            status_code=400,
            detail="Nothing to update"
        )

    if employee.name is not None:
        if not employee.name.strip():
            raise HTTPException(
                status_code=400,
                detail="Employee name is required"
            )
        employees[employee_id]["name"] = employee.name

    if employee.department is not None:
        if not employee.department.strip():
            raise HTTPException(
                status_code=400,
                detail="Department is required"
            )
        employees[employee_id]["department"] = employee.department

    if employee.salary is not None:
        if employee.salary <= 0:
            raise HTTPException(
                status_code=400,
                detail="Salary must be greater than zero"
            )
        employees[employee_id]["salary"] = employee.salary
    
    return {
        "id": employee_id,
        **employees[employee_id]
    }

@app.delete(
    "/employees/{employee_id}",
    status_code=200
)
def delete_employee(employee_id: int):

    if employee_id not in employees:
        raise HTTPException(
            status_code=400,
            detail="Employee not found"
        )

    deleted_employee = employees.pop(employee_id)

    return {
        "message": "Employee deleted successfully",
        "employee": {
            "id": employee_id,
            **deleted_employee
        }
    }


from typing import Optional

@app.get(
    "/employees",
    response_model=list[EmployeeResponse],
    status_code=200
)
def get_all_employees(

    # Filtering
    department: Optional[str] = None,
    min_salary: Optional[int] = None,
    max_salary: Optional[int] = None,

    # Searching
    search: Optional[str] = None,

    # Sorting
    sort_by: Optional[str] = None,
    order: str = "asc",

    # Pagination
    page: int = 1,
    limit: int = 5

):
    # Pagination Validation

    if page < 1:
        raise HTTPException(
            status_code=400,
            detail="Page must be at least 1"
        )

    if limit < 1:
        raise HTTPException(
            status_code=400,
            detail="Limit must be at least 1"
        )

    result = []

    # Filtering + Searching

    for employee_id, employee in employees.items():

        # Department Filter
        if department is not None:

            if employee["department"].lower() != department.lower():
                continue

        # Minimum Salary
        if min_salary is not None:

            if employee["salary"] < min_salary:
                continue

        # Maximum Salary
        if max_salary is not None:

            if employee["salary"] > max_salary:
                continue

        # Search by Name
        if search is not None:

            if search.lower() not in employee["name"].lower():
                continue

        result.append(
            {
                "id": employee_id,
                **employee
            }
        )

    # Sorting

    if sort_by is not None:

        if sort_by not in ["name", "salary", "department"]:

            raise HTTPException(
                status_code=400,
                detail="Invalid sort field"
            )

        reverse = order.lower() == "desc"

        result.sort(
            key=lambda employee: employee[sort_by],
            reverse=reverse
        )

    start = (page - 1) * limit
    end = start + limit

    return result[start:end]