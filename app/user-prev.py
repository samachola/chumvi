class User:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def registerUser(name, email, password):
        if name == '' or email == '' or password == '':
            return {'status': False, 'message': 'Could not add user'}

        user = {}
        user['name'] = name
        user['email'] = email
        user['password'] = password

        return {'status': True, 'user': user}





############ Add/Get recipe previous nini
# @app.route('/category', methods=['GET', 'POST'])
# def category():
#     session['show'] = True
#     if request.method == 'GET':
#         return render_template("add_category.html")
#     else:        
#         response = Category.addCategory(request.form['title'])
#         if response['status']:
#             session['categories'] = response['categories']
#             return redirect(url_for('category'))
#         else:
#             return render_template("add_category.html", error = response['message'])



################################## Add / DELETE CATE
# @app.route('/category', methods=['GET', 'POST'])
# def category():
#     session['show'] = True
#     if request.method == 'GET':
#         return render_template("add_category.html")
#     else:        
#         response = Category.addCategory(request.form['title'])
#         new_category
#         if response['status']:
#             session['categories'] = response['categories']
#             return redirect(url_for('category'))
#         else:
#             return render_template("add_category.html", error = response['message'])

        
# @app.route('/delete_category/<int:id>')
# def deleteCategory(id):
#     resp = Category.deleteCategory(id)
#     message = None

#     if resp['status']:
#         session['categories'] = resp['categories']
#         return redirect(url_for('category'))
#     else:
#         message = "Item not found"
#         return render_template("add_category.html", error = message)