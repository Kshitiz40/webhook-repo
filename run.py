from app import create_app
# from pyngrok import ngrok
import os

app = create_app()

if __name__ == '__main__': 
    # if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
    #     public_url = ngrok.connect(5000)
    #     print(f" * Ngrok tunnel \"{public_url}\" -> \"http://localhost:5000\"")

    app.run(debug=True)
