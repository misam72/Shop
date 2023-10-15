from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from .managers import UserManager

''' Q: what is difference between AbstractBaseUser and AbstractUser in django?

In Django, both `AbstractBaseUser` and `AbstractUser` are abstract base classes that can be used to 
create custom user models. However, they have some key differences in terms of functionality and the 
amount of built-in features they provide:

1. `AbstractBaseUser`:
   - `AbstractBaseUser` is the more lightweight and minimalistic option of the two. It provides the
   core functionality required for a user model, but it does not include features such as permissions, 
   groups, or fields like `first_name` and `last_name`.
   - When using `AbstractBaseUser`, you need to define the necessary fields for a user model yourself.
   Typically, this includes fields like `email`, `password`, and any additional fields specific to your
   application.
   - You also need to implement two methods: `get_username()` and `set_password()`, which are used for 
   authentication and password management.
   - By using `AbstractBaseUser`, you have full control over the fields and behavior of the user model,
   but you need to handle additional functionalities, such as permissions and groups, yourself.

2. `AbstractUser`:
   - `AbstractUser` is a more feature-rich option that extends `AbstractBaseUser` and adds more
   functionality out-of-the-box.
   - `AbstractUser` includes commonly used fields like `username`, `first_name`, `last_name`, `email`,
   and more. It also provides features like password management, permissions, groups, and user-related 
   functionalities.
   - With `AbstractUser`, you can create a user model with a richer set of fields and features without
   having to define them yourself.
   - If the built-in fields and functionalities of `AbstractUser` align with your requirements, it can
   save you time and effort compared to using `AbstractBaseUser` and implementing everything from scratch.

In summary, `AbstractBaseUser` provides a minimalistic foundation for creating a custom user model,
allowing you to define the fields and behavior yourself. On the other hand, `AbstractUser` is a more 
comprehensive option that includes common user-related fields and features, reducing the need for manual
implementation. The choice between the two depends on the specific needs of your project and the level of
customization and control you require.
'''

class User(AbstractBaseUser):
    '''we do not need to define password field because it has been 
    declared in AbstractBaseUser class.'''
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=11, unique=True)
    full_name = models.CharField(max_length=101)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    
    objects = UserManager()
    
    '''The value of unique argument for USERNAME_FIELDs must be True.'''
    USERNAME_FIELD = 'phone_number'
    
    '''REQUIRED_FIELDS is only for when we create a superuser in Terminal 
    with 'python manage.py createsuperuser' command and developer 
    must enter them in terminal. here username is phone_number 
    and password will be asked by default by django and finally we 
    have to enter 3 fields: email, phone_number and password.'''
    REQUIRED_FIELDS = ['email', 'full_name']
    
    def __srt__(self):
        return self.email
    
    ''' Q: what are has_perm and has_module_perms methods?
    has_perm(self, perm, obj=None):
    This method is responsible for checking whether a user has a specific permission. It takes two 
    parameters:
        perm: This parameter represents the permission string that needs to be checked. 
        It typically follows the format "app_label.permission_codename". For example, "polls.add_poll".
        obj (optional): This parameter represents an optional object for which the permission is checked.
        It can be used when the permission is object-specific. If obj is not provided, the method assumes the permission is for a global scope.

    In the provided implementation, the has_perm method always returns True. This means that the 
    user is considered to have all permissions. This behavior can be customized based on your 
    application's requirements. By default, Django's authorization system checks this method to 
    determine whether a user has a particular permission.

    has_module_perms(self, app_label):
    This method is responsible for checking whether a user has permissions to access the given app
    module. It takes one parameter:
        app_label: This parameter represents the label of the app module for which the permissions
        are checked. The label is typically the name of the Django app.

    In the provided implementation, the has_module_perms method always returns True. This means that
    the user is considered to have permissions to access any app module. Similar to has_perm, this
    behavior can be customized based on your application's requirements.

    By overriding these methods in the User model, you can control the permission logic for your users.
    Depending on your application's needs, you can implement more sophisticated logic to determine 
    whether a user has a specific permission or module access based on their attributes, roles, or
    other criteria.
    '''
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    ''' Q: What is @property for?
    Treat method as a variable that the method has been executed (and returned a value). 
    Example:
        class Circle:
            def __init__(self, radius):
                self.radius = radius

            @property
            def diameter(self):
                return 2 * self.radius

            circle = Circle(5)
            print(circle.diameter)  # Output: 10
    '''
    @property
    def is_staff(self):
        return self.is_admin
