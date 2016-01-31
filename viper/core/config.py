# This file is part of Viper - https://github.com/viper-framework/viper
# See the file 'LICENSE' for copying permission.

import os
import sys
import shutil
import ConfigParser

from viper.common.out import *
from viper.common.objects import Dictionary

class Config:
    
    def __init__(self, file_name="viper", cfg=None):
        config_paths = [
            os.path.join(os.getcwd(), 'viper.conf'),
            os.path.join(os.getenv('HOME'), '.viper', 'viper.conf'),
            '/etc/viper/viper.conf'
        ]

        config_file = None
        for config_path in config_paths:
            if os.path.exists(config_path):
                config_file = config_path
                break

        if not config_file:
            print("Unable to find any config file!")
            sys.exit(-1)
        
        config = ConfigParser.ConfigParser()
        config.read(config_file)

        for section in config.sections():
            setattr(self, section, Dictionary())
            for name, raw_value in config.items(section):
                try:
                    if config.get(section, name) in ["0", "1"]:
                        raise ValueError

                    value = config.getboolean(section, name)
                except ValueError:
                    try:
                        value = config.getint(section, name)
                    except ValueError:
                        value = config.get(section, name)

                setattr(getattr(self, section), name, value)

    def get(self, section):
        """Get option.
        @param section: section to fetch.
        @return: option value.
        """
        try:
            return getattr(self, section)
        except AttributeError as e:
            print e
