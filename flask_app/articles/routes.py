from flask import Blueprint, render_template, redirect, url_for

articles = Blueprint("articles", __name__)

from flask_app.client import NaviNewsClient
import os

api_key = os.environ.get("NEWS_API_KEY")
if not api_key:
    raise ValueError("NEWS_API_KEY environment variable is not set")

news_client = NaviNewsClient(api_key)

from flask_app.forms import SearchForm


""" ************ View functions ************ """
'''
  <form class="" action="/" method="POST">
    {{ form.csrf_token }}
    {{ form.search_query(class="", placeholder="Search for a topic...") }}
    
    {{ form.submit(class="") }}
  </form>
'''

@articles.route("/", methods=["GET", "POST"])
def index():
    try:
        top_headlines, total_results = news_client.get_top_headlines()
    except ValueError as e:
        top_headlines = []  # Fallback in case of an error
        print(f"Error fetching top headlines: {e}")
    
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for("articles.query_results", query=form.search_query.data))
    
    
    return render_template("index.html", top_headlines=top_headlines, form=form)



@articles.route("/search-results/<query>", methods=["GET"])
def query_results(query):
    try:
        results, total_results = news_client.search_articles(query)
    except ValueError as e:
        results = []
        return render_template("query.html", error_msg=str(e))

    return render_template("query.html", results=results)
