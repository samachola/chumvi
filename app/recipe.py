recipes = []
class Recipe: 
    
    def __init__(self, title, ingredients, process):
        self.title = title
        self.ingredients = ingredients
        self.process = process

    def addRecipe(title, ingredients, process):
        if title == '' or process == '' or ingredients == '':
            return { 'status': False, 'msg': 'cannot add empty recipe'}
        else:
            recipe = {}
            recipe['title'] = title
            recipe['ingredients'] = ingredients
            recipe['process'] = process
            recipes.append(recipe)


            return { 'status': True, 'msg': 'recipe successfully added', 'recipes': recipes}

    
    def viewRecipe(id):
        for recipe in recipes:
            if recipe == recipes[id]:
                print(id)
                print(recipes[id])
                return {'status': True, 'recipe': recipe}
            else:
                return {'status': False, 'message': 'Recipe not found'}

    def deleteRecipe(id):
        for recipe in recipes:
            if recipe == recipes[id]:
                recipes.remove(recipe)

        print(recipes)      
        return {'status': True, 'recipes' : recipes}
