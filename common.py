import yaml
config_file_path = "config.yml"

def config():
    with open(config_file_path, 'r') as stream:
        try:
            parsed_yaml=yaml.safe_load(stream)
            #print(parsed_yaml)
        except yaml.YAMLError as exc:
            print(exc)
    return parsed_yaml