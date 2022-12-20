# Back-end for GPT Presentation Builder

## Setup: To run on your local machine run the following

### (1) Download virtual environment

1. run the following: `pip3 install virtualenv`

### (2) Setup the virtual environment

1. run the following:

```
python3 -m venv ./venv
source ./venv/bin/activate
pip3 install -r requirements.txt
```

### (3) Run the app

1. run the following: `python3 app.py`

## Misc

-   Read more about virtual environments and their importance [here](https://realpython.com/lessons/what-virtual-environments-are-good-for).
-   What does `source ./venv/bin/activate` do?
    -   source is a bash command that runs a file, the same way you’d use import to run your python module.1 bin/activate is the bash script being run.
    -   activates the virtual env in the current powershell
    -   some IDE's recognize the venv automatically (such as VSCode with the Python extension)
