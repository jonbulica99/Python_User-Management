from databases.sqlite import Sqlite


class Memory(Sqlite):
    __version__ = 0.1

    def __init__(self, *args, **kwargs):
        kwargs.pop("database")
        super().__init__(database="", dialect="sqlite", *args, **kwargs)
        self.check_if_enough_memory()

    def check_if_enough_memory(self, warn_percent=80, crit_percent=95, default=True):
        try:
            import psutil
            mem_percent = psutil.virtual_memory().percent
            if mem_percent > crit_percent:
                self.log.crit(
                    "Not enough system memory left (%s percent is being used).", mem_percent)
                del self
            elif mem_percent > warn_percent:
                self.log.warning(
                    "The OS is running out of memory. If the kernel kills this process, you data will disappear forever! (%s percent is being used).", mem_percent)
        except ImportError as e:
            self.log.warning(
                "Module psutil not found. Cannot check system memory before creating memory DB.")
        return default
