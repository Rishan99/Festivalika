

from entity.user_entity import UserEntity
from services.auth_service import AuthService
from services.general_service import GeneralService


a = AuthService()
authService = AuthService()
authService.registerUser(UserEntity("rishn","rishn","ddress",23,1,"pssword"))

