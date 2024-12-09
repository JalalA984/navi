# NaviNews – Navigate the World of News Effortlessly

NaviNews is a web application that allows users to explore current world news, search for topics of interest, and save their favorite searches and articles for easy access later.

## Deployed Website

Check out the live version of NaviNews here, make sure to let it load for ~50 seconds: [https://navinews.onrender.com/](https://navinews.onrender.com/)

### Notes:

- **Render Hosting**: Render automatically shuts down the server during periods of inactivity. If the website appears inactive, it might take about a minute to start up again.
- **MongoDB Cluster**: The MongoDB cluster might experience similar inactivity-related delays, though this should be rare.
- **API Issues**: Occasionally, you might encounter a Python Flask error due to something with the API. Simply refresh the page to resolve it.

## Run Locally

1. Download and install [Docker Desktop](https://www.docker.com/products/docker-desktop/).
2. Pull the Docker image by running the following command:

```bash
docker pull jalal984/navinews
```

## Project Overview

### Application Features

- Explore current world news.
- Search for specific topics of interest.
- Save and manage favorite articles and searches (for logged-in users only).

### Features for Logged-in Users

The following features are only available to logged-in users:

- **Save Articles**: Save news articles to revisit them later.
- **Favorite Topics**: Save searches or topics of interest for quick access.

Non-logged-in users can still browse and search for articles but cannot save any data.

### Forms in the Application

The application uses the following forms:

- **RegistrationForm**: For user registration (requires email, username, and password).
- **LoginForm**: For logging in existing users.
- **SearchForm**: To search for articles or topics.
- **SaveArticleForm**: To save a specific article.
- **PreferCategoryForm**: To mark a search or topic as a favorite.

### Routes and Blueprints

The application is structured into two blueprints:

1. **users Blueprint**:
   - `/login` – User login.
   - `/register` – User registration.
   - `/account` – User account management.

2. **articles Blueprint**:
   - `/saved-articles` – View saved articles.
   - `/favorite-categories` – View favorite topics.
   - `/search-results/query` – View search results.

### Database Structure

The application uses MongoDB to store and retrieve the following data:

- **User Model**:
  - Username, email, password.
  - Preferred categories (user-saved searches/topics).
- **SavedArticle Model**:
  - Article details, including title, URL, and content.
  - Reference to the user who saved the article.

## Third-Party Integrations

The application uses the NewsAPI to fetch news articles. This API provides the core functionality of exploring news topics.

### API Limitations:

- **Request Limits**: The API allows a maximum of 100 requests per day. So don't load the page 100 times... (Future optimizations will probably reduce unnecessary requests.)
- **Article Delay**: The API serves articles with a 24-hour delay, meaning you will see articles from the previous day.

## Final Notes

NaviNews is designed to simplify the way users interact with global news. Whether you're looking for breaking news or diving deep into a specific topic, NaviNews makes it easy to stay informed.

Enjoy exploring! 😊








