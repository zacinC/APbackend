from fastapi import APIRouter

home_router = APIRouter()


@home_router.get('/')
def get_home():
    return "Dobrodošli na API autobuskog prevoza Crne Gore"
