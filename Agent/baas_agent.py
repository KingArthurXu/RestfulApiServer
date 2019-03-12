#!/bin/python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：      baas_agent
   Description:
   Author:          'Arthur Xu'
   date:            2019/3/11
-------------------------------------------------
   Change Activity:
   2019/3/11:     
-------------------------------------------------
"""
__author__ = 'Arthur Xu'
import nb_agent
import logging
from config import Config

config = Config()

logging.config.dictConfig(config.log_conf)
try:
    nb_agent.start()
except KeyboardInterrupt as e:
    logging.warning("stop server by user")



