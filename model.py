from google.appengine.ext import db


class Promotion(db.Model):
    company_keyname = db.StringProperty()
    company_name = db.StringProperty()
    company_url = db.StringProperty()
    company_about = db.TextProperty()

    promo_url = db.StringProperty()
    promo_code = db.StringProperty()
    promo_type = db.StringProperty(choices=["url", "code"])
    promo_note = db.TextProperty()
    promo_title = db.StringProperty(default="")

    created_at = db.DateTimeProperty(auto_now_add=True)
    modified_at = db.DateTimeProperty(auto_now=True)
