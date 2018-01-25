from .handlers import *

app = webapp2.WSGIApplication([
    webapp2.Route(template='/',
                  handler=PromotionHandler,
                  handler_method='fetch_all',
                  methods=['GET']),

    webapp2.Route(template='/promo/add',
                  handler=PromotionHandler,
                  handler_method='add',
                  methods=['POST']),

    webapp2.Route(template='/promo/update',
                  handler=PromotionHandler,
                  handler_method='update',
                  methods=['POST']),

    ('/([^/]+)?', PromotionHandler)  # Always keep this routing last
])
