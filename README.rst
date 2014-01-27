Tic Tac Toe
===========

A tic tac toe game that you can try to win, but you never will.

Dependencies
++++++++++++

In addition to Django and other Python dependences specified in requirements.pip, this project requires `nodejs <http://nodejs.org/>`_ (and ``npm``, which comes with node) in order to install and build the frontend files. Stylesheets and Javascript are compiled from less and coffeescript using Grunt.

Installation
++++++++++++
1. Clone this repo, and cd into its root directory.

2. Create a virtual environment, and activate it.

3. Install requirements with pip::

    pip install -r requirements.pip

4. Install node dependencies::

    npm install

5. Install bower dependencies::

    ./node_modules/.bin/bower install

6. Build the frontend files with Grunt::

    ./node_modules/.bin/grunt build

7. Start the server::

    ./manage.py runserver
