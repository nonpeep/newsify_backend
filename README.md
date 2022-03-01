# Newsify Backend
Backend for [Newsify](https://github.com/nonpeep/newsify_frontend). A Flask app hosted on [Cloud Run](https://cloud.google.com/run) as Docker container. 
It has three exposed endpoints: `/headlines`, `/predict`, and `/article`.

To get it running for testing purposes, simply clone the repository, `cd` into it, get the dependencies (listed in the Dockerfile) and run
```
flask run 
```

You can comment out the code for getting the model if you do not want to test the predictions. Otherwise, run `bootstrap.py` beforehand.
