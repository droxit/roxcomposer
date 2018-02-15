import os
import json
from mosaic import exceptions


config_identifier = 'DROXIT_MOSAIC_CONFIG'
# FixMe : path variable. Where's the config file? default_config = $PATH + '/services.json'
default_config = 'config.json'


# This class builds the core system config. It loads a json file, where the config parameters are set. You can access
# parameters with the get_item function
class MosaicConfig:
    def __init__(self, config_file=None):
        self.config = {}

        if config_file is None:
            config_file = default_config
            if config_identifier in os.environ:
                config_file = os.environ[config_identifier]

        try:
            f = open(config_file, 'r')
        except Exception as e:
            raise exceptions.ConfigError('unable to read the configuration file: {} - {}'.format(config_file, e)) from e

        try:
            self.config = json.load(f)
        except Exception as e:
            raise exceptions.ConfigError('unable to parse the configuration file: {} - {}'.format(config_file,e)) from e
        finally:
            f.close()

    # because you don't know the exact location of the item in the config this function will return the right value of
    # the config item passed with item_as_string
    def get_item(self, item_as_string):

        path = item_as_string.split('.')
        conf = self.config
        for p in path:
            if p in conf:
                conf = conf[p]
            else:
                raise exceptions.ParameterMissing("%s not present in the configuration" % item_as_string)

        return conf

    # returns a string representation of the config
    def to_json(self):
        return json.dumps(self.config)


if __name__ == "__main__":
    cc = MosaicConfig()

    print(cc.to_json())
