import configparser


def write_default_config():

    config = configparser.ConfigParser()

    config.add_section('keys.api.openai')
    config['keys.api.openai']['api_key'] = "FIXME"

    config.add_section('keys.api.gemini')
    config['keys.api.gemini']['api_key'] = "FIXME"

    with open("config.ini", 'w') as f:
        config.write(f)