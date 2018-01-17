import json
import logging
import traceback

import datetime
import webapp2
from google.appengine.ext.webapp import template

from .models import Promotion
import utils

from memcacheWrapper import memcachePlus


class PromotionHandler(webapp2.RequestHandler):
    def get(self, company):
        cache_key = "PromotionHandler.get.{}".format(company)
        cached_results = memcachePlus.get(cache_key)
        if cached_results:
            template_values = json.loads(cached_results)
        else:
            company_promo = Promotion.get(company_keyname=company)
            if not company_promo:
                self.error(404)
                return

            template_values = Promotion.get_json_object(company_promo[0])
            memcachePlus.set(cache_key, json.dumps(template_values))

        page = utils.template("promo.html", "Promotion/html")
        self.response.out.write(template.render(page, template_values))

    def fetch_all(self):
        cache_key = "PromotionHandler.fetch_all"
        cached_results = memcachePlus.get_multipart(cache_key)
        if cached_results:
            result = json.loads(cached_results)
        else:
            all_promo = Promotion.get()
            result = []
            for company_promo in all_promo:
                result.append(Promotion.get_json_object(company_promo))
            memcachePlus.set_multipart(cache_key, json.dumps(result))

        template_values = {"all_promo": result}

        page = utils.template("home.html", "Promotion/html")
        self.response.out.write(template.render(page, template_values))

    def add(self):
        user_info = utils.authenticate_user_account(self, email_list=["jigarbhatt93@gmail.com"])
        if not user_info:
            return

        self.response.headers['Content-Type'] = "application/json"
        self.response.headers['Access-Control-Allow-Origin'] = '*'

        try:
            cache_key = "PromotionHandler.fetch_all"
            promotion = Promotion()
            response = promotion.add(
                company_keyname=self.request.get("company_keyname", None),
                company_name=self.request.get("company_name", None),
                company_url=self.request.get("company_url", None),
                company_about=self.request.get("company_about", None),
                promo_url=self.request.get("promo_url", None),
                promo_code=self.request.get("promo_code", None),
                promo_type=self.request.get("promo_type", None),
                promo_note=self.request.get("promo_note", None),
            )
            memcachePlus.delete_multipart(cache_key)
            self.response.out.write(json.dumps({'success': True, 'error': [], 'response': response}))
        except Exception as e:
            self.response.out.write(json.dumps({'success': False, 'error': e.message, 'response': None}))
            logging.error(traceback.format_exc())
