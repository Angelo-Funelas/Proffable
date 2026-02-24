from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST
import json

@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({"detail": "CSRF cookie set"})

@require_POST
def login_view(request):
    try:
        data = json.loads(request.body)
    
        email = data.get('email')
        password = data.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({
                "message": "Login successful",
                "user": {"email": user.email, "id": user.id}
            })
        return JsonResponse({"detail": "Invalid credentials"}, status=401)
    except Exception as e:
        return JsonResponse({"detail": str(e)}, status=400)

def logout_view(request):
    logout(request)
    return JsonResponse({"detail": "Logged out"})