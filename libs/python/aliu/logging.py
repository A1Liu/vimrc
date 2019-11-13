import inspect, re, sys, os

def _get_logger_id(obj):
    if isinstance(obj, str):
        return (obj, None)
    elif hasattr(obj, '__call__'):
        filename = inspect.getsourcefile(obj)
        return (os.path.relpath(filename), obj.__name__)
    elif isinstance(obj, inspect.types.FrameType) or obj is None:
        if obj is None:
            obj = inspect.currentframe().f_back.f_back
        frame_info = inspect.getframeinfo(obj)
        if frame_info.function == '<module>':
            return (os.path.relpath(frame_info.filename), None)
        else:
            return (os.path.relpath(frame_info.filename), frame_info.function)
    else:
        raise AssertionError("Incorrect type passed for _get_logger (type=%s)" % (type(obj)))

class Logger(object):
    REGISTERED_LOGGERS = {}

    def __init__(self, obj = None):
        global _get_logger_id
        self.enabled = True
        self.id = _get_logger_id(obj)
        if self.id in Logger.REGISTERED_LOGGERS:
            raise AssertionError("Rebuilt existing logger.")
        else:
            Logger.REGISTERED_LOGGERS[self.id] = self
            if (self.id[0], None) not in Logger.REGISTERED_LOGGERS:
                Logger(obj = self.id[0])

    def get_prefix(self):
        if self.id[1] is None:
            return str(self.id[0])
        else:
            return ':'.join(self.id)

    def log(self, *args, sep = ' ', end = '\n'):
        if self.enabled:
            print(self.id[0], *args, sep = sep, end = end, file = sys.stderr)

def _get_logger(obj):
    id = _get_logger_id(obj if obj is not None else inspect.currentframe().f_back.f_back)
    if id in Logger.REGISTERED_LOGGERS:
        return Logger.REGISTERED_LOGGERS[id]
    return Logger(obj)

def get_logger(obj = None):
    return _get_logger(obj)

def configure_logger(obj = None, level = None):
    logger = _get_logger(obj)
    logger.level = level
    return logger

def disable_logger(obj = None):
    logger = _get_logger(obj)
    logger.enabled = False

def disable_logger(obj = None):
    logger = _get_logger(obj)
    logger.enabled = True

def log_function(func):
    logger = _get_logger(func)
    return func

def debug(*args, sep = ' '):
    logger = _get_logger(None)
    prefix = '%s ~ ' % inspect.getframeinfo( inspect.currentframe().f_back ).lineno
    message = sep.join(args)
    for line in message.split('\n'):
        logger.log(prefix + line)
