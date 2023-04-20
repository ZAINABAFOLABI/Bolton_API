from flask import Blueprint

venues = Blueprint("venues", __name__,
                   url_prefix="/mybolton/v1/venues")

@venues.get('/')
def get_venue_details():
    return {"venue":"Babbage Lab"}