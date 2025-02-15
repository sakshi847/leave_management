from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Employee, Leave, LeaveQuota
from .forms import LeaveForm
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User

from .forms import SignupForm

def is_admin(user):
    return user.is_staff or user.is_superuser

def signup(request):
    from .forms import SignupForm  
    
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            login(request, user)
            return redirect('login')
    else:
        form = SignupForm()
    
    return render(request, 'signup.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')  

def custom_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard') 
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'login.html')


@login_required
def dashboard(request):
    if request.user.is_staff:  
        leaves = Leave.objects.all()  
        return render(request, 'admin_dashboard.html', {'leaves': leaves})
    else:  
        leaves = Leave.objects.filter(employee=request.user) 
        return render(request, 'employee_dashboard.html', {'leaves': leaves})

@login_required
def apply_leave(request):
    if request.method == 'POST':
        form = LeaveForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.employee = request.user
            leave.save()
            return redirect('dashboard')
    else:
        form = LeaveForm()
    return render(request, 'apply_leave.html', {'form': form})


@login_required
@user_passes_test(is_admin)
def manage_leaves(request):
    leaves = Leave.objects.all().order_by('-start_date')  
    return render(request, 'manage_leaves.html', {'leaves': leaves})


@login_required
@user_passes_test(is_admin)

def approve_leave(request, leave_id):
    leave = get_object_or_404(Leave, id=leave_id)
    leave.status = 'approved'
    leave.approved_by = request.user
    leave.save()
    return redirect('manage_leaves')

@login_required
@user_passes_test(is_admin)

def reject_leave(request, leave_id):
    leave = get_object_or_404(Leave, id=leave_id)
    leave.status = 'rejected'
    leave.approved_by = request.user
    leave.save()
    return redirect('manage_leaves')


@login_required
def add_leave_quota(request):
    employees = User.objects.filter(is_staff=False)  
    leave_quotas = LeaveQuota.objects.all()

    if request.method == "POST":
        employee_id = request.POST.get("employee")
        sl_quota = request.POST.get("sl_quota")
        pl_quota = request.POST.get("pl_quota")
        cl_quota = request.POST.get("cl_quota")

        employee = get_object_or_404(User, id=employee_id)

        sl_quota = int(sl_quota) if sl_quota else 0
        pl_quota = int(pl_quota) if pl_quota else 0
        cl_quota = int(cl_quota) if cl_quota else 0

        leave_types = {
            "SL": sl_quota,
            "PL": pl_quota,
            "CL": cl_quota,
        }

        for leave_type, quota in leave_types.items():
            LeaveQuota.objects.update_or_create(
                employee=employee,
                leave_type=leave_type,
                defaults={
                    "total_quota": quota,
                    "used_quota": 0,
                    "remain_quota": quota, 
                },
            )

        return redirect("leave_quota")

    return render(request, "leave_quota.html", {"employees": employees, "leave_quotas": leave_quotas})


@login_required

def edit_leave(request, leave_id):
    leave = get_object_or_404(Leave, id=leave_id)
    if request.method == 'POST':
        form = LeaveForm(request.POST, instance=leave)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  
    else:
        form = LeaveForm(instance=leave)
    
    return render(request, 'edit_leave.html', {'form': form})