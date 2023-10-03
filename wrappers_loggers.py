import logging,os
from datetime import datetime

class LogWrapper(object):

    def __init__(self, level, filename, format):

        dirs =["logs"]

        for i in dirs:
            if not os.path.exists(i):
                os.makedirs(i)
                
    #memory_file = BytesIO()
        file_path = 'logs'
        for root, dirs, files in os.walk(file_path):
            if len(files)==5 and len(files)>=5:
                for file in files:
                    sub_file=os.path.join(root,file)
            else:
                if sub_file :=files[:-5]:
                    for i in sub_file:
                            sub_file=os.path.join(file_path,i)
                            os.remove(sub_file)

        logging.basicConfig(
        format=format,level=level,
        filename=f"logs/{datetime.utcnow().strftime('%Y-%m-%d')}.log"
        )
        self.log = logging.getLogger()

    def debug(self, message):
        self.log.debug(message)

    def info(self, message):
        self.log.info(message)

    def error(self, message):
        self.log.error(message)

    def warning(self, message):
        self.log.warning(message)
