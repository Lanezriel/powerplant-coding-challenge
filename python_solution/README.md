# powerplant-coding-challenge : Python solution

## How to install

Copy the repository to your machine

Check you have a python installed (I did it with 3.9.1 but this should be working with 3.7+)
If you desire, you can create your own venv with the following command :
`python -m venv path/to/env`

If you are using a venv, activate it by using :
`source <venv>/bin/activate` on Unix
`{venv}\Scripts\activate.bat` on Windows

Go to `./python_solution/`

Install the required libraries with :
`pip install -r requirements.txt`

(Make sure your cmd / bash has administrator priviledges to avoid any potential issue)

Once everything is installed, stay in the `./python_solution/` folder and run the following :
`python manage.py runserver localhost:8888`
The development server will launch
==> For this exercise I did not want to build a production version
==> Please note that for any production purpose, the `runserver` method should never be used

Go to your web browser and navigate to : `localhost:8888/productionplan`

You are now on the productionplan API View.

From this place, you can directly send your JSON objects (as well formated strings).
You can also use the http requests from any frontend. You just need to point (and have access) to the same adress in the localhost.

If you want the development server to be seen on the network, you could use this command instead :
`python manage.py runserver 0.0.0.0:8888`
This should do the job and you should be able to access the API from your network IP adress (in place of localhost or 0.0.0.0)