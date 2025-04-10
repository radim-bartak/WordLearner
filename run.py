from app import create_app
from app.config import Config

app = create_app()
config = Config("config.json")

if __name__ == "__main__":
    app.run(debug=config.DEBUG, port=config.PORT)
