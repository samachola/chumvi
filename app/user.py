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