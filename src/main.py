from utils.logger import init_logger
import uvicorn
from core.init_api import app
from core.config import settings
from core.init_api import app
from api import main_router

def main():
    init_logger()
    app.include_router(main_router)
    uvicorn.run(app, host=settings.API_HOST, port=settings.API_PORT)



if __name__ == "__main__":
    main()
