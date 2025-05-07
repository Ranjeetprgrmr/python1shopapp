from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.

'''
By using self to access the attributes of the class, you can write more concise and readable code, and avoid having to repeat the class name every time you want to access an attribute.
Without using self:
class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, passwrod=None):
        user = MyAccountManager.model(
            email=MyAccountManager.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )

        user.save(using=MyAccountManager._db)

        return user

'''
class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('User must have an email address')

        if not username:
            raise ValueError('User must have an username')
        # self refers to the instance of MyAccountManager
        # Accessing the Account model using self
        # self.model refers to the Account model
        user = self.model( 
            # Accessing the normalize_email method using self
            # self.normalize_email is a method of MyAccountManager
            email=self.normalize_email(email), 
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
         # Accessing the database connection using self._db
         # self._db refers to the database connection
        user.save(using=self._db) 
        return user
    
    def create_superuser(self, first_name, last_name, username, email, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user
    

class Account(AbstractBaseUser):
    first_name   = models.CharField(max_length=50)
    last_name    = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=50)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    #This line of code is creating an instance of the MyAccountManager class and assigning it to the objects attribute of the Account model.
    # In Django, the objects attribute is a special attribute that is used to manage the instances of a model. By default, Django creates a Manager instance for each model, which is used to interact with the database and perform CRUD (Create, Read, Update, Delete) operations.
    # In this case, the objects attribute is being overridden with an instance of the MyAccountManager class. This means that instead of using the default Manager instance, the Account model will use the custom MyAccountManager instance to manage its instances.
    # The MyAccountManager class is a custom manager that inherits from BaseUserManager. It provides a custom implementation of the create_user method, which is used to create new user instances.
    # By assigning the MyAccountManager instance to the objects attribute, the Account model is telling Django to use this custom manager to manage its instances.
    # Here's an example of how this works:
    # In this example, the create_user method of the MyAccountManager instance is called to create a new user instance.
    # By using a custom manager, you can customize the behavior of the objects attribute and provide additional functionality for managing instances of the Account model.
    # account = Account.objects.create_user(email='example@example.com', password='password123')
    objects = MyAccountManager()
    
    #1. __str__(self)
    # This method is a special method in Python that returns a string representation of the object. In this case, it returns the email attribute of the Account object.
    # When you print an instance of the Account class, Python will call this method to get a string representation of the object.
    # For example:
    # account = Account(email='example@example.com')
    # print(account)  # Output: example@example.com
    def __str__(self):
        return self.email
    
    
    #2. has_perm(self, perm, obj=None)
    #This method is used to check if the user has a specific permission. In this case, it simply returns True if the user is an admin (self.is_admin is True), and False otherwise.
    # The perm parameter is the permission being checked, and obj is an optional object that the permission is being checked against.
    # For example:
    # account = Account(email='example@example.com', is_admin=True)
    # print(account.has_perm('can_view_dashboard'))  # Output: True
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    
    #3. has_module_perms(self, add_label)
    # This method is used to check if the user has permission to access a specific module or app. In this case, it simply returns True, which means the user has access to all modules.
    # The add_label parameter is not used in this implementation.
    # For example:
    # account = Account(email='example@example.com')
    # print(account.has_module_perms('my_app'))  # Output: True
    def has_module_perms(self, add_label):
        return True
    
    

'''
In the code you provided, here are the instances and attributes:

**Instances:**

* `MyAccountManager` is a class, and when you create an instance of it, you get an object that has its own set of attributes and methods. For example: `account_manager = MyAccountManager()`
* `Account` is a class, and when you create an instance of it, you get an object that has its own set of attributes and methods. For example: `user = Account(email='example@example.com', username='example')`

**Attributes:**

* `MyAccountManager` has the following attributes:
	+ `create_user`: a method that creates a new user account
	+ `model`: an attribute that refers to the `Account` model
	+ `_db`: an attribute that refers to the database connection
* `Account` has the following attributes:
	+ `first_name`: a field that stores the user's first name
	+ `last_name`: a field that stores the user's last name
	+ `username`: a field that stores the user's username
	+ `email`: a field that stores the user's email address
	+ `phone_number`: a field that stores the user's phone number
	+ `date_joined`: a field that stores the date the user joined
	+ `last_login`: a field that stores the date the user last logged in
	+ `is_admin`: a field that stores a boolean indicating whether the user is an admin
	+ `is_staff`: a field that stores a boolean indicating whether the user is a staff member
	+ `is_active`: a field that stores a boolean indicating whether the user is active
	+ `is_superadmin`: a field that stores a boolean indicating whether the user is a super admin
	+ `USERNAME_FIELD`: an attribute that stores the field that is used as the username (in this case, the email address)
	+ `REQUIRED_FIELDS`: an attribute that stores a list of fields that are required when creating a new user account
	+ `objects`: an attribute that stores the `MyAccountManager` instance

Note that some of these attributes are methods, while others are fields or other types of attributes.

In the context of the `create_user` method, the `self` parameter refers to the instance of the `MyAccountManager` class, and the `user` variable refers to the instance of the `Account` class that is being created.

In the MyAccountManager class, the self parameter is used to refer to the instance of the class itself.

When you define a method inside a class, the first parameter is always self, which refers to the instance of the class. This is a convention in Python, and it's used to access the attributes and methods of the class.

In the create_user method, self refers to the instance of the MyAccountManager class. This means that self has access to all the attributes and methods of the MyAccountManager class.

Here are some examples of how self is used in the create_user method:

self.model: This refers to the Account model that is associated with the MyAccountManager instance.
self.normalize_email(email): This calls the normalize_email method on the MyAccountManager instance, passing the email parameter.
self._db: This refers to the database connection that is associated with the MyAccountManager instance.
By using self, the create_user method can access the attributes and methods of the MyAccountManager class, and use them to create a new user account.

'''