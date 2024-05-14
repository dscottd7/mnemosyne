from flask import Blueprint, render_template
views_route = Blueprint("views_route", __name__, template_folder='../templates')
from api.utils import summarize_client_portfolio

@views_route.get("/")
def chatbot_page():
    summary = summarize_client_portfolio()
    return render_template('index.html', summary=summary)