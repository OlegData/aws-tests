import constants


def get_config():
    config = {}
    config["ASSETS_BASE"] = "static"
    config["DEBUG"] = True
    config["ENVIROMENT"] = "DEV"
    config["PROJECT_PATH"] = ""
    config["SQLALCHEMY_DATABASE_URI"] = constants.DB_PATH
    config["SQLALCHEMY_ECHO"] = True
    config["SQLALCHEMY_RECORD_QUERIES"] = True
    config["SECKRET_KEY"] = constants.SECRET_KEY

    return config
