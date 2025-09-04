from django.shortcuts import get_object_or_404, redirect, render,HttpResponse
from .models import Employee,Role,Department
from datetime import datetime
from django.db.models  import Q

# Create your views here.
def index(request):
    return render(request,"index.html")
def all_emp(request):
    emps=Employee.objects.all()
    context={
        'emps':emps
    }
    print(context)
    return render(request,"view_all_emp.html",context)

def add_emp(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        Last_name = request.POST['last_name']
        dept_id = request.POST['department_id']
        role_id = request.POST['role_id']
        salary = request.POST['salary']
        bonus = request.POST['bonus']
        phone = request.POST['phone']

        # hire_date=request.POST['hire_date']

        try:
            department = Department.objects.get(id=dept_id)
            role = Role.objects.get(id=role_id)
            emp = Employee(first_name=first_name, Last_name=Last_name,
                           dept_id=dept_id, role=role,salary=salary,bonus=bonus,phone=phone)
            emp.save()
            return HttpResponse("Employee added successfully!")
        except Department.DoesNotExist:
            return HttpResponse("Invalid Department selected.")
        except Role.DoesNotExist:
            return HttpResponse("Invalid Role selected.")

    departments = Department.objects.all()
    roles = Role.objects.all()
    return render(request, "add_emp.html", {"departments": departments, "roles": roles})


def remove_emp(request,emp_id=None):
    if emp_id:
        try:
            emp_to_be_removed=Employee.objects.get(id=emp_id)
            emp_to_be_removed.delete()
            return HttpResponse("Employee Removed successfull")
        except:
            return HttpResponse("Ple Enter A Valid Emp ID")
    emps=Employee.objects.all()
    context={
        "emps":emps
    }
    return render(request,'remove_emp.html',context)
    
    
    # return render(request,"remove_emp.html")
# def filter_emp(request):
#     if request.method=="POST":
#         name=request.POST['name']
#         dept=request.POST['dept']
#         role=request.POST['role']
#         emps=Employee.objects.all()
#         if name:
#             emps=emps.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))
#         if dept:
#             emps=emps.filter(dept__name__icontains=dept)
#         if role:
#             emps=emps.filter(role__name__icontains=role)
#         context={
#             'emps':emps
#         }
#         return render(request,"view_all_emp.html",context)
#     elif request.method=="GET":
#         return render(request,"filter_emp.html")
#     else:
#         return HttpResponse("An Exception Occurs")
        
        
def filter_emp(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        dept = request.POST.get('dept', '')
        role = request.POST.get('role', '')

        emps = Employee.objects.all()

        if name:
            emps = emps.filter(Q(first_name__icontains=name) | Q(Last_name__icontains=name))
        if dept:
            emps = emps.filter(dept__name__icontains=dept)  
        if role:
            emps = emps.filter(role__name__icontains=role)

        return render(request, "view_all_emp.html", {"emps": emps})

    return render(request, "filter_emp.html")


from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Employee, Department, Role

def update_emp(request):
    if request.method == "POST":
        name = request.POST.get("name")

       
        if name and "first_name" not in request.POST:
            try:
                emp = Employee.objects.get(first_name__iexact=name)
                departments = Department.objects.all()
                roles = Role.objects.all()
                return render(request, "update_emp.html", {
                    "emp": emp,
                    "departments": departments,
                    "roles": roles,
                })
            except Employee.DoesNotExist:
                return HttpResponse("No employee found with this name")

       
        elif name and "first_name" in request.POST:
            emp_id = request.POST.get("emp_id")
            emp = get_object_or_404(Employee, id=emp_id)
            emp.first_name = request.POST.get("first_name")
            emp.Last_name = request.POST.get("last_name")
            emp.salary = request.POST.get("salary")
            emp.bonus = request.POST.get("bonus")
            emp.phone = request.POST.get("phone")
            emp.dept_id = request.POST.get("department_id")
            emp.role_id = request.POST.get("role_id")
            emp.save()
            return HttpResponse("Employee Updated Successfully!")

    
    return render(request, "update_emp.html")
