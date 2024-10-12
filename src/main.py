import structlog
import flask
import blueprints
from sqlalchemy.orm import configure_mappers

import config, constants, database


logger = structlog.get_logger(__name__)


def _rollback_after_exception(requesr_or_exception):
    if isinstance(requesr_or_exception, Exception):
        database.db.session.rollback()


def _bind_path():
    logger.bind(flaks_path=flask.request)


def _log_status_code(response):
    # if response.status_code == 200:
    #     logger.info("response_status_code", status_code=response.status_code)
    # else:
    logger.warn("response_status_code", status_code=response.status_code)


def create_app():
    app = flask.Flask(
        import_name=constants.APP_NAME,
        static_folder=constants.STATIC_FOLDER,
        template_folder=constants.TEMPLATE_FOLDER,
    )
    app.config.update(config.get_config())
    app.secret_key = app.config["SECKRET_KEY"]
    blueprints.register_blueprints(app)
    # https://flask.palletsprojects.com/en/2.3.x/api/#flask.Flask.session_interface
    app.session_interface = flask.sessions.SecureCookieSessionInterface()
    # https://flask.palletsprojects.com/en/2.3.x/api/#flask.Flask.permanent_session_lifetime
    app.permanent_session_lifetime = 120

    # Initialize the SQlAlchemy mappers to avoid a race condition where the auditing colums are pertially initialized
    configure_mappers()
    database.db.init_app(app)

    app.teardown_request(_rollback_after_exception)
    # app.before_request(_bind_app)
    # app.before_request(_bind_user_id)
    app.before_request(_bind_path)
    app.after_request(_log_status_code)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
