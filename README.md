# JPGTODATEDDIR 1.0.0

Console utility for copying jpg and tiff images to dated folders in source.

### Prerequisites

* Python 3
* virtualenv
* ExifRead

### Installing

On working directory:

```
# linux
virtualenv --clear -p python3 venv
# win
virtualenv --clear venv

# linux
source venv/bin/activate
# win
venv\Scripts\activate.bat

pip install -r requirements.txt
```

### Usage

```
usage: jpgtodir.py [-h] [-p POSTFIX] source_dir

Move JPG and TIFF images to dated directory

positional arguments:
  source_dir            Source directory

optional arguments:
  -h, --help            show this help message and exit
  -p POSTFIX, --postfix POSTFIX
                        Postfix for dated directory
```

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/grspectre/jpgtodateddir/tags). 

## Authors

* **Anton Shanaurin** - *Initial work* - [grspectre](https://github.com/grspectre)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
