import logging
logging.basicConfig(
    level=logging.DEBUG,
    filename="Logs/Running_Log",
    filemode='a',
    format='%(asctime)s %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

