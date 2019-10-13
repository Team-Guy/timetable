# Timetable
As a student @ubb you want to have a beautiful, simple way to view your schedule, featuring a 
calendar display and two-week support. Keeping track of your location will allow us to give you 
the shortest route to your next activity. This application will adapt to your preferences and 
changes as time passes. It's exactly what a timetable should be.

## Set up DJANGO environment

### I. WINDOWS
##### 1. Install Python 3.7

  - download Python 3.7.x

  - on the installation wizard click add Python 3.7 to PATH and hit 'Customize Installation' then click next

  - under Advanced Options check 'Install for all users' and modify the path to 'C:\Python37'

  - after the installation is complete open the terminal and type in:

```bash
python -V => you should have the installed python displayed here
```

##### 2. Install virtualenvwrapper-win

```bash
pip install pypiwin32
pip install virtualenvwrapper-win
```

 - open up the terminal in C:\Python37\Scripts and type:

```bash
pip install pypiwin32
```


##### 3. Create virtual environment

```bash
mkvirtualenv -p 3 timetable-venv
```

 - to activate the virtual environment type:

```bash
workon timetable-venv
```

 - to deactivate the virtual environment type:

```bash
deactivate
```

##### 4. Make sure you have postgres installed on your machine + development

##### 5. Clone the project, install the requirements in your environment
(while the environment is activated)
```bash
pip install -r requrements.txt
```

##### 6. Configure the environment variables for your database (username and password)


 - to test that DJANGO was installed correctly clone this repository and type the following command in terminal at the location where the project is located:

```bash
python manage.py runserver
```

 - the expected outcome is:

```bash
Performing system checks...

System check identified no issues (0 silenced).

You have unapplied migrations; your app may not work properly until they are applied.
Run 'python manage.py migrate' to apply them.

October 09, 2019 - 15:50:53
Django version 2.2, using settings 'mysite.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

 - now navigate to localhost:8000 and see the server running


### II. Ubuntu

#####1.Installing & Making python 3.7.x global interpretor
 - If you already have it skip ( python --version to check )
 - Below is just one method to set this up, there are plenty of others
 
 Install pyenv from here : https://github.com/pyenv/pyenv#installation ( environment for using different version of python on your pc )
 ```bash
 pyenv install 3.7.x
```

Put this in your ~/.bashrc file -> makes this python global

```bash
if which pyenv > /dev/null; then
  eval "$(pyenv init -)"
  if which python3 > /dev/null; then
    PY3=`pyenv whence python3`
    pyenv global $PY3
    pyenv shell $PY3
  fi
fi
```

#####2.Installing virtualenv

```bash
pip install virtualenv
```

#####3.Make sure u have postgres installed and run this commands:

```bash
sudo apt-get install python-psycopg2
sudo apt-get install libpq-dev
```

#####4. Clone the project, create a virtual environment in which we will keep the dependencies, activate it and install dependendices
(In project root or wherever)
```bash
virtualenv timetable-venv
source timetable-venv/bin/activate
pip install -r requrements.txt
```

Now you can follow the windows steps from 6 :D.