from fastapi.responses import HTMLResponse
from fastapi import FastAPI


app = FastAPI

def baseHTML():
    contentHTML = """
    <!DOCTYPE html>
    <title>{% block title %}{% endblock %} - Flaskr</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
    <nav>
      <h1>Page Register</h1>
      <ul>
        {% if g.user %}
        <li><span>{{ g.user['username'] }}</span>
        <li><a href="{{ url_for('auth.logout') }}">Log Out</a>
          {% else %}
        <li><a href="{{ url_for('auth.register') }}">Register</a>
        <li><a href="{{ url_for('auth.login') }}">Log In</a>
          {% endif %}
      </ul>
    </nav>
    <section class="content">
      <header>
        {% block header %}{% endblock %}
      </header>
      {% for message in get_flashed_messages() %}
      <div class="flash">{{ message }}</div>
      {% endfor %}
      {% block content %}{% endblock %}
    </section>
    """

    return HTMLResponse(content=contentHTML, status_code=200)

@app.get("/page/", response_class=HTMLResponse)
async def base():
    return baseHTML()