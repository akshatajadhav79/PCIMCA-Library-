from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class post(models.Model):
    title=models.CharField(max_length=225)
    email=models.EmailField(max_length=255)
    password=models.CharField(max_length=255)
    
    
class Author(models.Model):
    aid = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    catid = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class Book(models.Model):
    bid = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    isbn = models.CharField(max_length=13, unique=True)
    published_date = models.DateField()
    total_copies = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField(default=1)
    Bpic = models.ImageField(upload_to='book_pics/', blank=True, null=True)

    def __str__(self):
        return f"{self.title} by {self.author.name}"
    
class MyUser(models.Model):
    uid = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    full_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)  # Consider using AbstractUser for security
    email = models.EmailField(unique=True)
    pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    contact = models.CharField(max_length=15, blank=True, null=True)
    is_active = models.BooleanField(blank=True)
    
    # Category choices
    CATEGORY_CHOICES = [
        ('student', 'Student'),
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
    ]
    category = models.CharField(
        max_length=10, 
        choices=CATEGORY_CHOICES, 
        default='student', 
        blank=True, 
        null=True  # Allows empty values in the database
    )

    def __str__(self):
        return f"{self.username} ({self.get_category_display() if self.category else 'No Category'})"

   
class IssuedBookRecord(models.Model):
    brid = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    Issueded_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    returned_date = models.DateTimeField(null=True, blank=True)

    def is_overdue(self):
        """Check if the book is overdue."""
        return self.returned_date is None and self.due_date < timezone.now()

    def calculate_fine(self):
        """Calculate fine based on overdue days."""
        if self.is_overdue():
            overdue_days = (timezone.now().date() - self.due_date.date()).days
            fine_amount = overdue_days * 10  # ₹10 per day
            return fine_amount
        return 0

    def save(self, *args, **kwargs):
        """Automatically create or update fine if overdue."""
        super().save(*args, **kwargs)
        if self.is_overdue():
            fine, created = Fine.objects.get_or_create(borrow_record=self, defaults={'amount': self.calculate_fine()})
            if not created:
                fine.amount = self.calculate_fine()
                fine.save()

    def __str__(self):
        return f"{self.user.username} borrowed {self.book.title}"
    
class Fine(models.Model):
    fid = models.BigAutoField(primary_key=True)
    borrow_record = models.OneToOneField(IssuedBookRecord, on_delete=models.CASCADE, related_name="fine")
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Fine of {self.amount} for {self.borrow_record.user.username}"

class Contact(models.Model):
    cid = models.BigAutoField(primary_key=True)
    cname = models.CharField(max_length=100,blank=False)
    cemail = models.EmailField(max_length=100,unique=True)
    cmsg = models.TextField()
   