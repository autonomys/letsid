# run_app.py (located in letsid-draft/)
from src.web.app import app

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
