import logging


def log_config(log_file):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s : %(levelname)s  %(message)s',
                        datefmt='%Y-%m-%d %A %H:%M:%S', filename=log_file, filemode='w')

    console_log_handler = logging.StreamHandler()
    console_log_handler.setLevel(logging.INFO)
    console_log_handler.setFormatter(logging.Formatter('%(asctime)s : %(levelname)s  %(message)s'))
    logging.getLogger().addHandler(console_log_handler)
