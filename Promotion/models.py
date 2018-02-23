import logging

import copy

import model
import utils


class Promotion(object):
    def __init__(self):
        pass

    def add(self, **data):
        self.check_validity(method='add', data=data)

        promotion, promotion_exists = self.get_datastore_entity(data)
        if promotion_exists:
            raise Exception("Promotion already present. Try updating it instead!")

        promotion.put()

    def update(self, **data):
        self.check_validity(method='update', data=data)

        data = {key: val for key, val in data.iteritems() if val != None}

        promotion = model.Promotion.get_by_key_name(data["company_keyname"])
        if not promotion:
            raise Exception("Promotion does not exist. Try adding it instead!")

        json_object = self.get_json_object(promotion)
        old_json_object = copy.copy(json_object)
        json_object.update(data)

        if json_object == old_json_object:
            raise Exception('No Changes Made')

        promotion, promotion_exists = self.get_datastore_entity(json_object)
        promotion.put()

    @staticmethod
    def get(debug=False, **filters):
        query_string = "select * from Promotion"

        filters = {key: val for key, val in filters.iteritems() if val != None}

        i = 0
        for field in filters:
            if type(filters[field]) == bool:
                field_value = str(filters[field])
            else:
                field_value = "'{}'".format(filters[field])

            if i == 0:
                query_string += " where "

            if i < len(filters) - 1:
                query_string += "{}={} and ".format(field, field_value)
            else:
                query_string += "{}={}".format(field, field_value)
            i += 1

        response = utils.fetch_gql(query_string)
        if debug:
            logging.error("Query String: %s\n\n Response Length: %s" % (query_string, len(response)))

        return response

    @staticmethod
    def get_json_object(datastore_entity):
        json_object = {
            "company_keyname": datastore_entity.company_keyname,
            "company_name": datastore_entity.company_name,
            "company_url": datastore_entity.company_url,
            "company_about": datastore_entity.company_about,
            "promo_url": datastore_entity.promo_url,
            "promo_code": datastore_entity.promo_code,
            "promo_type": datastore_entity.promo_type,
            "promo_note": datastore_entity.promo_note,
            "promo_title": datastore_entity.promo_title,
            "promo_running_status": datastore_entity.promo_running_status,
            "modified_at": datastore_entity.modified_at.strftime('%Y-%m-%d %H:%M'),
            "created_at": datastore_entity.created_at.strftime('%Y-%m-%d %H:%M'),
        }

        return json_object

    @staticmethod
    def get_datastore_entity(json_object):
        promotion_exists = True
        datastore_entity = model.Promotion.get_by_key_name(json_object["company_keyname"])
        if not datastore_entity:
            promotion_exists = False
            datastore_entity = model.Promotion(key_name=json_object["company_keyname"])

        datastore_entity.company_keyname = json_object["company_keyname"]
        datastore_entity.company_name = json_object["company_name"]
        datastore_entity.company_url = json_object["company_url"]
        datastore_entity.company_about = json_object["company_about"]
        datastore_entity.promo_url = json_object["promo_url"]
        datastore_entity.promo_code = json_object["promo_code"]
        datastore_entity.promo_type = json_object["promo_type"]
        datastore_entity.promo_note = json_object["promo_note"]
        datastore_entity.promo_title = json_object["promo_title"]
        datastore_entity.promo_running_status = json_object.get("promo_running_status", True)

        return datastore_entity, promotion_exists

    @staticmethod
    def check_validity(method, data):
        error = []

        if error:
            raise Exception(error)
