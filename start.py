import os
import uvicorn


if __name__ =='__main__':
    os.system('python manage.py runserver')                                             #1 Отладочную версия
    #uvicorn.run("config.asgi:application", host="127.0.0.1", port=8000, reload=True)   #2 Вариант на uvicorn


