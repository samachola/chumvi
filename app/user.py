import uuid

class User():
    """ User class user to add new users and add categories. """
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
        self.categories = []
        self.recipes = []


        
class Category():
    """ Add Categories to a user. """
    def __init__(self, title, description):
        self.title = title
        self.description = description
        self.id = uuid.uuid4()
        

      
class Recipe(object):
    """ Adds  Recipe to a category. """
    def __init__(self, name, category, ingredients, process):
        self.name = name
        self.ingredients = ingredients
        self.process = process
        self.category = category