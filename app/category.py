categories = []
class Category:

    def __init__(self, title):
        self.title = title

    def addCategory(title):
        if title == '':
            return {'status': False, 'message': 'Category title is required'}
        else:            
            category = {}
            category['title'] = title
            categories.append(category)
            return {'status': True, 'categories': categories}

    def deleteCategory(id):
        status = False
        for category in categories:
            if category == categories[id]:
                status = True
                categories.remove(category)

        return {'status': status, 'categories': categories}