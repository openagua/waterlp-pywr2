import json
from os import environ
from .hydra import Hydra

hydra = Hydra()


class connection(object):

    def __init__(self, args=None, scenario_ids=None, log=None):
        self.url = args.data_url
        self.filename = args.filename
        self.app_name = args.app_name
        self.user_id = int(args.user_id)
        self.log = log

        self.network_id = int(args.network_id)
        self.template_id = int(args.template_id) if args.template_id else None

        if args.filename:
            with open(args.filename) as f:
                data = json.load(f, object_hook=JSONObject)
                self.network = data.get('network')
                self.template = data.get('template')
                self.template_attributes = data.get('template_attributes')
                self.template_id = self.template.get('id')

        else:
            get_network_params = dict(
                include_data='Y',
                scenario_ids=scenario_ids,
                summary='N'
            )
            if self.template_id:
                get_network_params.update({'template_id': self.template_id})
            self.network = hydra.get_network(self.network_id, **get_network_params)
            self.template_id = self.template_id or self.network.layout.get('active_template_id')
            self.template = self.template_id and hydra.get_template(self.template_id)

        dimensions = hydra.get_dimensions()
        dimensions = json.loads(dimensions) # TODO: fix hydra - this should return json, not string
        self.dimensions = {d['id']: d for d in dimensions}

        # create some useful dictionaries
        # Since pyomo doesn't know about attribute ids, etc., we need to be able to relate
        # pyomo variable names to resource attributes to be able to save data back to the database.
        # the res_tattrs dictionary lets us do that by relating pyomo indices and variable names to
        # the resource attribute id.

        # dictionary to store resource attribute dataset types
        self.attr_meta = {}

        # dictionary for looking up attribute ids

    def get_basic_network(self):
        if self.filename:
            return self.network
        else:
            return hydra.get_network(self.network.id, include_data=False, summary=False, include_resources=False)

    # def get_template_attributes(self):
    #     if self.filename:
    #         return self.template_attributes
    #     else:
    #         return self.call('get_template_attributes', {'template_id': self.template.id})
    #

    def dump_results(self, resource_scenario):
        return hydra.update_scenario(resource_scenario, return_summary=True)


class JSONObject(dict):
    def __init__(self, obj_dict):
        for k, v in obj_dict.items():
            self[k] = v
            setattr(self, k, v)
