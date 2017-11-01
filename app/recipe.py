recipes = []
class Recipe: 
    
    def __init__(self, title, ingredients, process):
        self.title = title
        self.ingredients = ingredients
        self.process = process

    def addRecipe(title, category, ingredients, process):
        if title == '' or category == '' or process == '' or ingredients == '':
            return { 'status': False, 'msg': 'cannot add empty recipe, all fields are requied'}
        else:
            recipe = {}
            recipe['title'] = title
            recipe['category'] = category
            recipe['ingredients'] = ingredients
            recipe['process'] = process
            recipes.append(recipe)


            return { 'status': True, 'msg': 'recipe successfully added', 'recipes': recipes}

    def updateRecipe(id, title, category, ingredients, process):
        
        response = {}
        recipee = {}
        for recipe in recipes:
            if recipe == recipes[id]:
                
                recipes.remove(recipe)
                recipee['title'] = title
                recipee['category'] = category
                recipee['ingredients'] = ingredients
                recipee['process'] = process 
                recipes.append(recipee)  

                response['status'] = True          
            else:
                response['status'] = False
                
        return { 'status':response['status'], 'recipes': recipes }
        
    
    def viewRecipe(id):
        response = {}
        for recipe in recipes:
            if recipe == recipes[id]:
                response['status'] = True
                response['id'] = id
                response['title'] = recipe['title']
                response['category'] = recipe['category']
                response['ingredients'] = recipe['ingredients']
                response['process'] = recipe['process']                
            else:
                response['status'] = False
                
        return response

    def deleteRecipe(id):
        for recipe in recipes:
            if recipe == recipes[id]:
                recipes.remove(recipe)

        print(recipes)      
        return {'status': True, 'recipes' : recipes}
