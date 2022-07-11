from fastapi.responses import HTMLResponse
from fastapi import FastAPI


app = FastAPI()


def loginHTML():
    contentHTML = """
    {% extends 'base.html' %}

    {% block header %}
    <h1>{% block title %}Log In{% endblock %}</h1>
    {% endblock %}
    
    {% block content %}
    <form method="post">
      <label for="username">Username</label>
      <input name="username" id="username" required>
      <label for="password">Password</label>
      <input type="password" name="password" id="password" required>
      <input type="submit" value="Log In">
    </form>
    {% endblock %}
    """

    return HTMLResponse(content=contentHTML, status_code=200)

@app.get("/login/", response_model=HTMLResponse)
async def login():
    return loginHTML()
