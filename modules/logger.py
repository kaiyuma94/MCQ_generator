import logging
from pathlib import Path
from typing import Optional
from .config_manager import load_config

def setup_logger(name: str) -> logging.Logger:
    config = load_config()
    logger = logging.getLogger(name)
    logger.setLevel(config['logging']['level'])

    if not logger.handlers:
        formatter = logging.Formatter(config['logging']['format'])
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # File handler
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)
        
        file_handler = logging.FileHandler(log_dir / 'processing.log')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
    return logger