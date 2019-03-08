#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Arthur Xu'
import os
import logging.config
from manage import app
from flask_cors import CORS


CORS(app)
# logging.getLogger('flask_cors').level = logging.DEBUG

from baas.others.upload import site_blueprint
from baas.endpoints import api_blueprint
app.register_blueprint(blueprint=api_blueprint)
app.register_blueprint(blueprint=site_blueprint)

if __name__ != '__main__':

    # [logger]root redirect to gunicorn.error
    gunicorn_logger = logging.getLogger('gunicorn.error')
    logging.getLogger().handlers = gunicorn_logger.handlers
    logging.getLogger().setLevel(gunicorn_logger.level)
    logging.info("redirect logging to here ...")

    # [logger]app.logger redirect to gunicorn.error
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    app.logger.info("redirect app.logger to here ...")

if __name__ == '__main__':
    flask_host = os.getenv("FLASK_HOST") if os.getenv("FLASK_HOST") else '0.0.0.0'
    flask_port = os.getenv("FLASK_PORT") if os.getenv("FLASK_PORT") else '5000'
    # flask_debug = app.config['DEBUG']
    # application.run(host=flask_host, port=int(flask_port), debug=bool(flask_debug))
    # app.run(host=flask_host, port=int(flask_port), debug=app.config['DEBUG'])
    app.run(host=flask_host, port=int(flask_port), debug=False)
    # flask_ssl_context = os.getenv("FLASK_SSL_CONTEXT") if os.getenv("FLASK_SSL_CONTEXT") else 'None'
    # app.run(ssl_context=flask_ssl_context, host=flask_host, port=int(flask_port), debug=bool(flask_debug))
    # 证书玩法
    # app.run(debug=True, ssl_context=(
    #     "server/server-cert.pem",
    #     "server/server-key.pem")
    # )


