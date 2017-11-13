import uuid

class User(object):
    """ User class user to add new users and add categories. """
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
        self.categories = []
        self.recipes = []

    def addCategory(self, title):
        self.categories.append(title)
        return {'status': True, 'msg': "Category added successfully"}

    def removeCategory(self, title):
        self.categories.pop(title)
        return {'status': True}
    def addRecipe(self, name, category, ingredients, process):
        
        recipe = {}
        recipe['name'] = name
        recipe['category'] = category
        recipe['ingredients'] = ingredients
        recipe['process'] = process

        self.recipes.append(recipe)
        return {'status': True}

        
class Category(object):
    """ Add Categories to a user. """
    def __init__(self, title):
        self.title = title
        self.id = uuid.uuid4()

      
class Recipe(object):
    """ Adds  Recipe to a category. """
    def __init__(self, name, category, ingredients, process):
        self.name = name
        self.ingredients = ingredients
        self.process = process
        self.category = category