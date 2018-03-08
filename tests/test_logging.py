import os
import sys


def _gw_logging_cfg(log_file):
    return {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': "%(asctime)s - %(levelname)-5s - %(message)s"
            },
            'debug': {
                'format': "%(asctime)s - %(levelname)-5s - %(name)-40s - %(message)-80s - %(module)s:%("
                          "funcName)s(%(lineno)s)"
            },
        },
        'handlers': {
            'console_stdout': {
                'formatter': 'standard',
                'class': 'logging.StreamHandler',
                'stream': sys.stdout,
                'level': 'INFO'
            },
            'file': {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "debug",
                "filename": log_file,
                "maxBytes": 1024000,
                "backupCount": 3,
                'level': 'INFO'
            },
        },
        'loggers': {
            '': {
                'handlers': ['console_stdout'],
                'level': 'INFO',
                'propagate': False
            },
            'groundwork': {
                'handlers': ['console_stdout', 'file'],
                'level': 'INFO',
                'propagate': False
            },
        }
    }


def test_logging_file(basicApp, tmpdir):
    log_file = os.path.join(str(tmpdir), "test.log")
    app = basicApp
    # set up logging in the config, with log level INFO
    app.config.set('GROUNDWORK_LOGGING', _gw_logging_cfg(log_file))
    app._configure_logging(app.config.get("GROUNDWORK_LOGGING"))

    debug_message = "This is a test debug message."
    info_message = "This is a test info message."
    app.log.debug(debug_message)
    app.log.info(info_message)

    # verify the contents of the log file
    with open(log_file) as lf:
        log = lf.read()
    # at log level INFO, the DEBUG message should not be there
    assert log.find(debug_message) == -1
    # the INFO message should be there
    assert log.find(info_message) > 0


def test_logging_console(basicApp, tmpdir, capsys):
    log_file = os.path.join(str(tmpdir), "test.log")
    app = basicApp
    # set up logging in the config, with log level INFO
    app.config.set('GROUNDWORK_LOGGING', _gw_logging_cfg(log_file))
    app._configure_logging(app.config.get("GROUNDWORK_LOGGING"))

    debug_message = "This is a test debug message."
    info_message = "This is a test info message."
    app.log.debug(debug_message)
    app.log.info(info_message)

    out, err = capsys.readouterr()
    # at log level INFO, the DEBUG message should not be there
    assert out.find(debug_message) == -1
    # the INFO message should be there
    assert out.find(info_message) > 0
