import uvicorn

from backend import app

if __name__ == "__main__":
    uvicorn.run(app, debug=True)
