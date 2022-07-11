from fastapi.responses import HTMLResponse
from fastapi import APIRouter


app = APIRouter()


@app.get("/createUser/", response_model=HTMLResponse)
async def register():
    contentHTML = """
        {% extends 'base.html' %}

        {% block header %}
        <h1>{% block title %}Register{% endblock %}</h1>
        {% endblock %}

        {% block content %}
        <form method="post">
          <label for="username">Username</label>
          <input name="username" id="username" required>
          <label for="password">Password</label>
          <input type="password" name="password" id="password" required>
          <input type="submit" value="Register">
        </form>
        {% endblock %}
        """

    return HTMLResponse(content=contentHTML)
