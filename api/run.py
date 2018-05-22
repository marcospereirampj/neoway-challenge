# -*- coding: utf-8 -*-
"""
Startup da application.
"""


from config import create_app

application = create_app('config.default.Config')

if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True, port=5000, use_reloader=True)