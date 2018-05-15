import time
import logger
while True:
    log = logger.Logger()
    log.print_status()
    time.sleep(60.0)
    print("****************************************************")
