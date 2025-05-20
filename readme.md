# DataHobbit

Just a simple tool that creates dataclasses from JSON files by assessing the JSON schema structure and 
building typed dataclasses into a .py file

Should be as simple as calling the program with `python ${PATH TO DATAHOBBIT}`, using one of the provided args
as seen below.

*Hasn't been tested yes, so don't @ me*

### Requirements
_______
>Python 3.13+

### Installation
______

COMING SOON

### Command Syntax
_____

cd {DIRECTORY}
`$ python data_hobbit.py -h`

```optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Direct system path to a JSON file (default: ${CWD}/sample.json)
  -o OUTPUT, --output OUTPUT
                        Directory the place output .py file with Dataclass (default: ${CWD}/sample.py)
  -d DIRECTORY, --directory DIRECTORY
                        Directory to JSON files, will parse all files within into data classes. (default: ${CWD}/sample.json)
  -n NAME, --name NAME  Name of parent Dataclass (default: GeneratedDataclass)
  -ad APPLY_DEFAULTS, --apply_defaults APPLY_DEFAULTS
                        Apply default values for all fields using the values within provided JSON file (default: None)
```