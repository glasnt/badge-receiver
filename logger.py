from datetime import datetime
import json
import logging
import sys

import json_logging

# c.f. https://github.com/thangbn/json-logging-python/blob/master/example/custom_log_format.py
class CloudLoggingFormatter(logging.Formatter):
    """Custom formatter for Google Cloud Logging
    """
    def get_exc_fields(self, record):
        if record.exc_info:
            exc_info = self.format_exception(record.exc_info)
        else:
            exc_info = record.exc_text
        return {'python.exc_info': exc_info}

    @classmethod
    def format_exception(cls, exc_info):
        return ''.join(traceback.format_exception(*exc_info)) if exc_info else ''

    def format(self, record):
        json_log_object = {
            "timestamp": datetime.utcnow().isoformat(),
            "severity": record.levelname,
            "message": record.getMessage(),
            "caller": record.filename + "::" + record.funcName
        }
        json_log_object['data'] = {
            "python.logger_name": record.name,
            "python.module": record.module,
            "python.funcName": record.funcName,
            "python.filename": record.filename,
            "python.lineno": record.lineno,
            "python.thread": record.threadName,
            "python.pid": record.process
        }
        if hasattr(record, 'props'):
            json_log_object['data'].update(record.props)

        if record.exc_info or record.exc_text:
            json_log_object['data'].update(self.get_exc_fields(record))

        return json.dumps(json_log_object)

def getJSONLogger(name):
    json_logging.init_non_web(custom_formatter=CloudLoggingFormatter, enable_json=True)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler(sys.stdout))
    return logger

def main():
    logger = getJSONLogger("json-logging-sample")
    logger.info("This is info level log.")
    logger.warning("This is warning level log.")
    logger.error("This is error level log.")

if __name__ == '__main__':
    main()
