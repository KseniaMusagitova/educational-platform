from fastapi import FastAPI
import uvicorn
from fastapi.routing import APIRouter
from sqlalchemy import Column, Boolean, String


from api.handlers import user_router


"""block with api routes"""

# create instance of the app
app = FastAPI(title="education-platform") #создание приложения


# create the instance for the routes
main_api_router = APIRouter()

# set routes to the app instance
main_api_router.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(main_api_router)

if __name__ == "__main__":
    # run app on the host amd port
    uvicorn.run(app, host="0.0.0.0", port=8001)


