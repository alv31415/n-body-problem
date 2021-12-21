# n-body-problem
Investigation of the N-Body problem via numerical methods. This branch focuses on producing a wesbite from the project, which explains the problem, and gives functionality to plot simulations. The website is up and running at https://nbody-89ffd.web.app . I used a React frontend (hosted in `firebase`), and a Django backend (hosted in `heroku`).

## Running the Server

This app uses a ```django``` backend. As is typical, a virtual environment is used. 
If we have called the virtual environment ```backend```, and we have created the virtual environemnt using:
```
python3 -m venv backend
```
we can activate it using:
```
source backend/bin/activate
```
Once this is done, we navigate to ```nbodyBACKEND``` and execute:
```
python3 manage.py runserver
```

## Running the React App

To run the React App, we need to have ```npm``` installed. Then once we are in the `nbody-frontend` directory, just execute:
```
npm start
```
Currently, the React App is made to run with the backend at https://nbody-api.herokuapp.com/api/.

## The N-Body Simulation

The simulation files are still in this branch, and can be found at https://github.com/alv31415/n-body-problem/tree/website/backend/nbodyBACKEND/sim .
