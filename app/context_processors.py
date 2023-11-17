def is_auth(request):
    user_auth = request.session.get("isAuthenticated")
    role = request.session.get("role")

    return {
        "user_auth": user_auth,
        "role": role
    }