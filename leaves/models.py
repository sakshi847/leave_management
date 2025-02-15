from django.db import models
from django.contrib.auth.models import User

class Employee(models.Model):
    name = models.CharField(max_length=100)

class LeaveQuota(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    sl_quota = models.FloatField(default=0)
    pl_quota = models.FloatField(default=0)
    cl_quota = models.FloatField(default=0)

    def __str__(self):
        return f"{self.employee.name} - SL: {self.sl_quota}, PL: {self.pl_quota}, CL: {self.cl_quota}"


class Leave(models.Model):
    LEAVE_TYPES = [
        ('PL', 'Privilege Leave'),
        ('CL', 'Casual Leave'),
        ('SL', 'Sick Leave'),
        ('LWP', 'Leave Without Pay'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=3, choices=LEAVE_TYPES)
    reason = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    total_days = models.IntegerField(null=False, blank=False) 
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_leaves')
    
    def save(self, *args, **kwargs):
        if self.start_date and self.end_date:
            self.total_days = (self.end_date - self.start_date).days + 1  
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.employee.username} - {self.leave_type} ({self.status})"

class LeaveQuota(models.Model):
    LEAVE_TYPES = [
        ('PL', 'Privilege Leave'),
        ('CL', 'Casual Leave'),
        ('SL', 'Sick Leave'),
        ('LWP', 'Leave Without Pay'),
    ]
    
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=3, choices=LEAVE_TYPES)
    total_quota = models.IntegerField()
    used_quota = models.IntegerField(default=0)
    remain_quota = models.IntegerField()
    
    def save(self, *args, **kwargs):
        self.remain_quota = self.total_quota - self.used_quota
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.employee.username} - {self.leave_type} Quota"

