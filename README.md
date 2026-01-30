# UI Link

Pleae use this link to view the minimal UI for the github actions stored in DB: [UI Link](https://action-repo.vercel.app/)

## Constraint

The backend is deployed on render free tier - therefore it becomes inactive when not used for sometime, please open this URL and wait for 2 minutes so that the backend can start and provide data and recieve data as well from the github action-repo webhook events. 

Thank You
*******************

# Dev Assessment - Webhook Receiver

Please use this repository for constructing the Flask webhook receiver.

*******************

## Setup

* Create a new virtual environment

```bash
pip install virtualenv
```

* Create the virtual env

```bash
virtualenv venv
```

* Activate the virtual env

```bash
source venv/Scripts/activate
```

* Install requirements

```bash
pip install -r requirements.txt
```

* Run the flask application (In production, please use Gunicorn)

```bash
python run.py
```

* The endpoint is at:

```bash
POST http://127.0.0.1:5000/webhook/receiver
```

You need to use this as the base and setup the flask app. Integrate this with MongoDB (commented at `app/extensions.py`)

*******************