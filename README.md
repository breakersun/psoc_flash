# psoc_flash
rewirte psoc flash tool with python for PSoC4 family, based on official python COM interface examples


## Install

1. install official psoc [programmer](https://www.dropbox.com/s/rls5xz9d9bv63cr/PSoCProgrammerSetup_3.29.1_b4659_0.exe?dl=0)
2. install python 3.10 and setting python paths
3. pip install -r requirements.txt

## Usage

```
python flash.py ccg3pa path/to/hexfile.hex
```

or

```
python flash.py ccg5 path/to/hexfile.hex
```

if pre-compiled executables are used:

```
flash.exe ccg3pa path/to/hexfile.hex
flash.exe ccg5 path/to/hexfile.hex
```

## NOTE

It's still under development, so please report bugs and suggestions.
