from flask import Flask
from mutant_detector.controllers.mutant_controller import mutant_bp
import os

app = Flask(__name__)

# Registrar el blueprint
app.register_blueprint(mutant_bp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))


