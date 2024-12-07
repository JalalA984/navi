from flask import Blueprint, render_template, redirect, url_for, request, flash

articles = Blueprint("articles", __name__)

from flask_app.client import NaviNewsClient, Article
import os

api_key = os.environ.get("NEWS_API_KEY")
if not api_key:
    raise ValueError("NEWS_API_KEY environment variable is not set")

news_client = NaviNewsClient(api_key)

from flask_app.forms import SearchForm, SaveArticleForm, PreferCategoryForm
from flask_app.models import SavedArticle
from flask_login import login_required, current_user


""" ************ View functions ************ """

@articles.route("/", methods=["GET", "POST"])
def index():
    try:
        top_headlines, total_results = news_client.get_top_headlines()
    except ValueError as e:
        top_headlines = []  # Fallback in case of an error
        print(f"Error fetching top headlines: {e}")
    
    search_form = SearchForm()
    save_form = SaveArticleForm()  # Create a SaveArticleForm instance
    
    if search_form.validate_on_submit():
        return redirect(url_for("articles.query_results", query=search_form.search_query.data))
    
    return render_template("index.html", top_headlines=top_headlines, search_form=search_form, save_form=save_form)



@articles.route("/search-results/<query>", methods=["GET", "POST"])
def query_results(query):
    try:
        results, total_results = news_client.search_articles(query)
    except ValueError as e:
        results = []
        return render_template("query.html", error_msg=str(e), search_form=SearchForm(), query=query)

    save_form = SaveArticleForm()
    prefer_category_form = PreferCategoryForm()  # Create an instance of PreferCategoryForm

    return render_template("query.html", results=results, search_form=SearchForm(), save_form=save_form, prefer_category_form=prefer_category_form, query=query)




@articles.route("/save-article", methods=["POST"])
@login_required
def save_article():
    form = SaveArticleForm()

    if form.validate_on_submit():
        # Check if the article with the same title and URL already exists for the current user
        existing_article = SavedArticle.objects(
            user=current_user,
            title=form.title.data,
            url=form.url.data
        ).first()

        if existing_article:
            flash("This article is already saved.")
        else:
            # Create and save the new SavedArticle object
            saved_article = SavedArticle(
                user=current_user,
                title=form.title.data,
                description=form.description.data,
                url=form.url.data,
                source=form.source.data,
                
            )
            try:
                saved_article.save()
                flash("Article saved successfully!")
            except Exception as e:
                flash(f"Error saving article: {str(e)}")
    
    return redirect(request.referrer)  # Redirect back to the previous page



@articles.route("/saved-articles", methods=["GET"])
@login_required
def saved_articles():
    try:
    
        
        # Retrieve all saved articles for the current user
        saved_articles = SavedArticle.objects(user=current_user)
        if not saved_articles:
            print("No saved articles found for the current user.")
        
        return render_template("saved_articles.html", saved_articles=saved_articles, title="Saved Articles")
    except Exception as e:
        print(f"Error: {str(e)}")  # Print the error to the console for debugging
        flash(f"Error retrieving saved articles: {str(e)}")
        return redirect(url_for("articles.index"))
    
    




@articles.route("/favorite-category", methods=["POST"])
@login_required
def favorite_category():
    form = PreferCategoryForm()

    if form.validate_on_submit():
        category = form.category.data.strip().lower()  # Get the category from the form

        if not category:
            flash("Category cannot be empty.")
            return redirect(request.referrer)

        # Add category to the current user's preferred categories if not already present
        if category not in current_user.preferred_categories:
            current_user.preferred_categories.append(category)
            try:
                current_user.save()  # Save the updated user document
                flash(f"Category '{category}' added to your preferences!")
            except Exception as e:
                flash(f"Error saving category: {str(e)}")
        else:
            flash("This category is already in your preferences.")
    
    return redirect(request.referrer)  # Redirect back to the previous page




@articles.route("/favorite-categories", methods=["GET"])
@login_required
def favorite_categories():
    try:
        preferred_categories = current_user.preferred_categories  # Retrieve categories from the current user
        return render_template("favorite_categories.html", categories=preferred_categories)
    except Exception as e:
        print(f"Error: {str(e)}")
        flash(f"Error retrieving favorite categories: {str(e)}")
        return redirect(url_for("articles.index"))
