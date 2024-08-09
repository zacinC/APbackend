from fastapi import APIRouter

home_router = APIRouter()


@home_router.get('/', include_in_schema=False)
def get_home():
    return "Dobrodošli na API autobuskog prevoza Crne Gore"
