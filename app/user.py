import uuid

class User(object):
    """ User class user to add new users and add categories. """
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
        self.categories = []

    def addCategory(self, title):
        self.categories.append(title)
        return {'status': True, 'msg': "Category added successfully"}
        
class Category(object):
    """ Add Categories to a user. """
    def __init__(self, title):
        self.title = title
        self.id = uuid.uuid4()
        self.recipes = []
        
    def addRecipe(self, recipe):
        self.recipes.append(recipe)
      
class Recipe(object):
    """ Adds  Recipe to a category. """
    def __init__(self, name, ingredients, process):
        self.name = name
        self.ingredients = ingredients
        self.process = process