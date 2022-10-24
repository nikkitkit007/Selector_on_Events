from server.__main__ import app
from configurations.default import DefaultSettings

if __name__ == "__main__":
    settings = DefaultSettings()
    print("---", settings.POSTGRES_PORT)
    app.run(port=8080)
