from django.db import models
from account.models import Account

# Create your models here.

class Field(models.Model):
    field = models.CharField(max_length=150)

    def __str__(self):
        return self.field

class Role(models.Model):
    role = models.CharField(max_length=150)

    def __str__(self):
        return self.role

class Industry(models.Model):
    industry = models.CharField(max_length=150)

    def __str__(self):
        return self.industry

class Discipline(models.Model):
    discipline = models.CharField(max_length=150)

    def __str__(self):
        return self.discipline

class State(models.Model):
    state = models.CharField(max_length=150)

    def __str__(self):
        return self.state

class Region(models.Model):
    region = models.CharField(max_length=150)

    def __str__(self):
        return self.region

class Qualification(models.Model):
    qualification = models.CharField(max_length=150)

    def __str__(self):
        return self.qualification


class Company(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    reg_no = models.CharField(max_length=100)
    status = models.BooleanField(default=False)
    type = models.CharField(max_length=30)
    affiliation = models.CharField(max_length=30)
    industry = models.CharField(max_length=50)
    web_link = models.URLField(max_length=400)
    address = models.CharField(max_length=300)
    phone_number = models.CharField(max_length=19)
    email = models.EmailField()
    # logo = models.ImageField(null=True, blank=True, upload_to='company_logo')
    description = models.CharField(max_length=2000)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    position_title = models.CharField(max_length=70)
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    qualification = models.CharField(max_length=70)
    employment_type = models.CharField(max_length=50)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    city = models.CharField(max_length=30)
    min_exp = models.IntegerField()
    max_exp = models.IntegerField()
    currency = models.CharField(max_length=20)
    term = models.CharField(max_length=20)
    min_salary = models.IntegerField()
    max_salary = models.IntegerField()
    app_deadline = models.CharField(max_length=30)
    dead_date = models.DateField()
    description = models.CharField(max_length=4000)
    draft = models.BooleanField(default=False)
    pinned_post = models.BooleanField(default=False)
    featured_post = models.BooleanField(default=True)
    free_post = models.BooleanField(default = False)
    status = models.CharField(max_length=30, blank=True, null=True)
    date_posted = models.DateField(auto_now_add=True)
    #addon
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE)
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)


    def __str__(self):
        return self.position_title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=50)
    email = models.EmailField()
    comment_content = models.CharField(max_length=1000)
    date_commented = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user_name

class Payment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=20)
    order_ref = models.CharField(max_length=50)
    payment_method = models.CharField(max_length=30)
    amount_paid = models.IntegerField()
    credits_received = models.IntegerField()
    status = models.BooleanField()     #Paystack status options
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id


class Invoice(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    number = models.CharField(max_length=50)
    pay_method = models.CharField(max_length=30)
    date_created = models.DateField(auto_now_add=True)
    credits = models.IntegerField()
    price = models.IntegerField()
    status = models.CharField(max_length=60)

    def __str__(self):
        return str(self.date_created)


class Transactions(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    job_title = models.ForeignKey(Post, on_delete=models.CASCADE)
    trans_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.trans_date)