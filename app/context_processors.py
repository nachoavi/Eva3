def is_auth(request):
    user_auth = request.session.get("isAuthenticated")

    return {
        "user_auth": user_auth
    }