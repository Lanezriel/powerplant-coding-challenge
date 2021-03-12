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

## Testing

If you want to test it using tests I wrote, go to `./python_solution/` folder and run the following command :
`python manage.py test`

This will use `./python_solution/productionplan/tests.py` file to run tests defined (as functions) inside the test class called `ProductionplanTest`

## Information about previous version

At first I thought I had to set `Powerplant Pmax` in the response instead of delivered `MWh as P` that is why I probably misunderstood and failed on first try.
In fact the `Max delivered MWh par Powerplant` I calculated was correct, I just misunderstood the value requested in the response.

Example: `Wind turbine` with a `pmax = 150` and `60%` wind ==> `Max MWh delivered = 90`

I thought I had to say `will work at full potential (=> 150) to deliver the maximum 90 MWh possible`, which I guess was a wrong understanding of the exercise.

It has now been fixed. As my understanding evolved.