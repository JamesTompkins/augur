from flask import Flask, jsonify, request, Response
import click, os, json, requests, logging
from workers.pull_request_worker.pull_request_worker import GitHubPullRequestWorker
from workers.util import create_server, WorkerGunicornApplication

def main():
    """ Declares singular worker and creates the server and flask app that it will be running on
    """
    app = Flask(__name__)
    app.worker = GitHubPullRequestWorker()

    create_server(app)
    WorkerGunicornApplication(app).run()

    if app.worker._child is not None:
        app.worker._child.terminate()
    try:
        requests.post('http://{}:{}/api/unstable/workers/remove'.format(broker_host, broker_port), json={"id": config['id']})
    except:
        pass

    os.kill(os.getpid(), 9)
