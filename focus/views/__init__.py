from focus import app
from . import slide
# register all the blueprint here

app.register_blueprint(slide.main)
