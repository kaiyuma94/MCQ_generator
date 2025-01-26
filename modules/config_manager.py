import yaml
import os
from pathlib import Path
from dotenv import load_dotenv
from typing import Dict

def load_config() -> Dict:
    # Load environment variables
    load_dotenv()
    
    config_path = Path(__file__).parent.parent / 'config' / 'config.yml'
    
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found at {config_path}")
        
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
            
        # Override API key from environment variable
        config['openai']['api_key'] = os.getenv('OPENAI_API_KEY')
        
        return config
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML in config file: {str(e)}")
    except Exception as e:
        raise Exception(f"Error loading config: {str(e)}")