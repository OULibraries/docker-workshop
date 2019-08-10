import os
from flask import Flask, flash, render_template, redirect, request, url_for
from redis import Redis
from redis.exceptions import ConnectionError
from forms import GuestbookForm

app = Flask(__name__)
app.secret_key = "DSeoN5aPVSbEsOwaDDBly3h9KZ4N665lPwkdP0qE"

# Read redis connection details from the environment.
redis_host = os.environ.get("REDIS_HOST", "localhost")
redis_port = os.environ.get("REDIS_PORT", "6379")
guest_field = "guests"

@app.route('/')
def congrats():
    """
    The Flask app route for /
    Returns a congratulations message.

    Returns
    -------
    str
        A congratulations message.
    """
    return "Awesome! You just deployed a Flask app in a Docker container!"

@app.route('/guestbook')
def view_guestbook():
    """
    The Flask app route for /guestbook
    Displays the current guestbook.

    Returns
    -------
    html
        The HTML for the /guestbook path.
    """
    if redis_available():
        # Connect to Redis
        redis_conn = connect_to_redis()
        guests = [guest.decode("utf-8") for guest in redis_conn.lrange(guest_field, 0, -1)]
        return render_template('guestbook.html', guests=guests)
    else:
        return handle_redis_err()

@app.route('/guestbook/sign', methods=['GET', 'POST'])
def sign_guestbook():
    """
    The Flask app route for /guestbook/sign
    Allows a user to sign the guestbook.

    Returns
    -------
    html
        The HTML for the /guestbook/sign path depending upon the HTTP
        verb used.
    """
    if redis_available():
        gb_form = GuestbookForm()
        if request.method == "POST":
            # Handle guestbook signing.
            redis_conn = connect_to_redis()
            name = request.form['name']
            guest_num = redis_conn.rpush(guest_field, name)
            flash(f"Thanks for signing the guestbook, {name}! You are guest number {guest_num}.")
            return redirect(url_for('view_guestbook'))
        # Render the guestbook signing form.
        return render_template('form.html', form=gb_form, template="form-page")
    else:
        return handle_redis_err()
    

def connect_to_redis():
    """
    Establishes a connection to the Redis instance defined by the REDIS_HOST
    and REDIS_PORT environment variables.

    Returns
    -------
    Redis
        A configured Redis connection.
    """
    return Redis(host=redis_host, port=redis_port, db=0)

def redis_available():
    """
    Determines if a connection can be established to the Redis instance defined
    by the REDIS_HOST and REDIS_PORT environment variables.

    Returns
    -------
    bool
        True if a connection to the Redis instance can be established. False
        otherwise.
    """
    try:
        redis = Redis(host=redis_host, port=redis_port, db=0)
        redis.ping()
        return True
    except ConnectionError as err:
        app.logger.error(f"Error connecting to Redis!\n{err}")
    return False

def handle_redis_err():
    """
    Returns an error message when a connection to Redis cannot be established.

    Returns
    -------
    str
        An error message stating that a connection to Redis could not be 
        established.
    """
    return (
        f"Can't connect to Redis at {redis_host}:{redis_port}!"
        " See logs for more details."
    )
    