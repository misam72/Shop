from django.contrib.auth.models import BaseUserManager


'''Q: What are managers in django models?
    In Django, managers are a fundamental part of models and provide an interface 
    for interacting with the database. Managers act as intermediaries between the database
    and the models, allowing you to perform queries and retrieve data from the database.

Here are the key points about managers in Django models:

1. Default Manager:
   - Every Django model has a default manager, which is automatically created if you don't specify 
   a custom manager explicitly.
   - The default manager is accessed using the `objects` attribute of the model class.
   - The default manager provides methods like `all()`, `filter()`, `get()`, and `create()` to 
   perform common database operations.
   - You can customize the default manager by creating a custom manager class and assigning
   it to the `objects` attribute of the model.

2. Custom Managers:
   - Django allows you to define custom managers to encapsulate complex query logic or provide 
   additional methods.
   - Custom managers are created by defining a manager class that inherits from `django.db.models.Manager`.
   - By defining custom methods in the manager class, you can add query functionality tailored to
   your specific needs.
   - Custom managers can be assigned to attributes in the model class, allowing you to access them
   directly from the model instances.

3. Chaining Querysets:
   - Managers return `QuerySet` objects, which represent the results of a database query.
   - QuerySets are chainable, meaning you can apply multiple query methods in a sequence to
   narrow down the results.
   - This allows you to construct complex queries by combining filters, ordering, and other 
   query operations.

4. Related Managers:
   - Django automatically creates related managers for relationships defined in models, such as
   foreign keys or many-to-many fields.
   - For example, if a `Book` model has a foreign key relationship to an `Author` model, Django
   creates a `book_set` attribute in the `Author` model to access related books.
   - Related managers provide methods like `add()`, `remove()`, and `set()` to manage the
   relationship between objects.

Managers are powerful tools in Django that enable you to interact with the database and perform 
various operations efficiently. They provide a high-level interface to query and manipulate data, 
allowing you to focus on your application's logic rather than dealing with raw SQL queries.
'''
class UserManager(BaseUserManager):
    def create_user(self, phone_number, email, full_name, password):
         if not phone_number:
             raise ValueError('user must have a phone number')
         if not email:
             raise ValueError('user must have an email')
         if not full_name:
             raise ValueError('user must have full name.')
         
         '''1.self.model is the model that we gave UserManager object to its object variable and 
         here is the User model.
         2.For email we checking it with normalize_email().'''
         user = self.model(phone_number=phone_number, 
                           email=self.normalize_email(email),
                           full_name=full_name)
         ''' with set_password() method password will be hashed. we will not save them
         raw/without hashing.'''
         user.set_password(password)
         user.save(using=self._db)
         return user
     
    def create_superuser(self, phone_number, email, full_name, password):
         user = self.create_superuser(phone_number, email, full_name, password)
         user.is_admin = True
         user.save(using=self._db)
         return user
     