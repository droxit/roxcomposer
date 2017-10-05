#
#!/usr/bin/env python3

import os
import json
from mosaic import exceptions


config_identifier = 'DROXIT_MOSAIC_CONFIG'
# FixMe : path variable. Where's the config file? default_config = $PATH + '/services.json'
default_config = '/home/marta/dev/mosaic/mosaic/example/services.json'


# This class builds the core system config. It loads a json file, where the config parameters are set. You can access
# parameters with the get_item function
class MosaicConfig:
    def __init__(self, config_file=None):
        self.config = {}

        if config_file is None:
            config_file = default_config
            if config_identifier in os.environ:
                config_file = os.environ[config_identifier]

        f = open(config_file, 'r')
        self.config = json.load(f)
        f.close()

    # because you don't know the exact location of the item in the config this function will return the right value of
    # the config item passed with item_as_string
    def get_item(self, item_as_string):

        print(item_as_string)

        path = item_as_string.split('.')
        conf = self.config
        for p in path:
            if p in conf:
                conf = conf[p]
            else:
                raise exceptions.ParameterMissingException("%s not present in the configuration" % item_as_string)

        return conf

    # returns a string representation of the config
    def to_json(self):
        return json.dumps(self.config)


if __name__ == "__main__":
    cc = MosaicConfig()

    print(cc.to_json())