import configparser
config = configparser.ConfigParser()

print(config.read("test.ini"))

print(config.sections())

config['p']