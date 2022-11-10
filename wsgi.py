from server.__main__ import app
from configurations.default import DefaultSettings

if __name__ == "__main__":
    settings = DefaultSettings()
    app.run(port=8080)
