# n-body-problem
Investigation of the N-Body problem via numerical methods

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
