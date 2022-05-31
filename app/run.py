from app import app #cause __init__.py is present so app folder is a library now

# remember to command line run export FLASK_APP=run.py then export FLASK_ENV=development when building and export FLASK_ENV=production when deploying
# in windows use set instead of export
if __name__ == '__main__':
    app.run()