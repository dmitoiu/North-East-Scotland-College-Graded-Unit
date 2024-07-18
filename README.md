# North East Scotland College Graded Unit Project

The Graded Unit Project is a Tailoring and Alterations tracker written in Python. 
It supports Databases such as Microsoft Access SQL, SQLite, MySQL and PostgreSQL.

## Graded Unit Project Compile-time Dependencies

* [Python](http://www.python.org) (2.7 required;)
* [WxPython](http://www.wxpython.org) (4.0.7+ required)
* [matplotlib](https://www.matplotlib.org/) (required)
* [PyODBC](https://www.github.com/mkleehammer/pyodbc) (4.0.28 required)
* [CX_Freeze](https://cx-freeze.readthedocs.io/en/stable) (optional)

## Installation

The [Graded Unit installation guides] includes instructions for installing the project as part of a local application.

### Standalone Installation

* Create the following tables according to the [Graded Unit Project database schema]:
 - `users`
 - `customers`
 - `tailors`
 - `projects`
 - `alterations`

## Running Graded Unit

### Run-time options:

* `python <path/to/main.py>` - Path to entry point file. If unspecified, the current working directory is used.