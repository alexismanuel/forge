import uvicorn
from fastapi import FastAPI
from app.config import AppConfig


app = FastAPI()


@app.get('/healthz')
def health_route():
    return 'OK'


@app.get('/')
def health_route():
    return 'Hello World !'


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=AppConfig.app_port, log_level=AppConfig.log_level)
