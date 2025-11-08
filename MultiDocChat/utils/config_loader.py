from pathlib import Path
import os
import yaml

def my_project_root()->Path:
    return Path(__file__).resolve().parents[1]



def load_config(config_file_path:str|None=None)->dict:
    env_path=os.getenv("CONFIG_PATH")
    if config_file_path is None:
        config_file_path=env_path or str(my_project_root()/"config"/"config.yaml")
    path=Path(config_file_path)
    if not path.is_absolute():
        path=my_project_root()/path
    if not path.exists():
        raise FileNotFoundError(f"config file not found at:{path}")
    with open(path,"r",encoding="utf-8") as file:
        return yaml.safe_load(file) or {}



print(load_config())# Use explicit path
# load_config()  

