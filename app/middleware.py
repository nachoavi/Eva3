from django.shortcuts import redirect

class AdminCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/dashboard/') and not request.session.get('isAuthenticated'):
            return redirect('/signin/')

        response = self.get_response(request)
        return response
    
class UserRoleCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/dashboard/') and request.session.get('role') != 2:
            return redirect('/')

        response = self.get_response(request)
        return response
    
    
