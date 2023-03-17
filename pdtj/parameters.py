import yaml
from yaml.loader import SafeLoader

try:
    # Open the file and load it
    with open("./.pdtj.yaml") as file:
        parameters = yaml.load(file, Loader=SafeLoader)

except FileNotFoundError:
    parameters = None

