from rest_framework_simplejwt.tokens import RefreshToken

# Service.py is used for writing business logic ,
# It improves Readibility , make things easier to understand

def refresh_function(user):
    user=user 
    return RefreshToken.for_user(user)

