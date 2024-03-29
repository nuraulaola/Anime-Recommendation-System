# 1. Import Libraries
"""

# Import necessary libraries for working with zip files
from zipfile import ZipFile

# Import machine learning libraries for clustering and evaluation metrics
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# Import library for data preprocessing (standard scaling)
from sklearn.preprocessing import StandardScaler

# Import plotting libraries for data visualization
import matplotlib.pyplot as plt
import seaborn as sns  # Seaborn is a statistical data visualization library

# Import numerical computation libraries
import numpy as np
import pandas as pd  # Pandas is a powerful data manipulation library

# Import libraries for measuring similarity and working with matrices
from sklearn.metrics.pairwise import cosine_similarity
import operator  # Operator module provides a set of convenient built-in functions

"""# 2. Load Data

## **2.1 Load Anime Data**
"""

url_animes = "https://raw.githubusercontent.com/nuraulaola/Anime-Recommendation-System/main/Datasets/anime.csv"
animes = pd.read_csv(url_animes)
animes.head()

"""**Content**

*   anime_id - myanimelist.net's unique id identifying an anime.

* name - full name of anime.

* genre - comma separated list of genres for this anime.

* type - movie, TV, OVA, etc.

* episodes - how many episodes in this show. (1 if movie).

* rating - average rating out of 10 for this anime.

* members - number of community members that are in this anime's
"group".

## **2.2 Load Ratings Data**
"""

url_ratings = "https://raw.githubusercontent.com/nuraulaola/Anime-Recommendation-System/main/Datasets/rating.csv"
ratings = pd.read_csv(url_ratings)
ratings = ratings[ratings["rating"] != -1]
ratings.head()

"""**Content**

* user_id - non identifiable randomly generated user id.

* anime_id - the anime that this user has rated.

* rating - rating out of 10 this user has assigned (-1 if the user watched it but didn't assign a rating).

# **3. Data Exploration**

## **3.1 Explore Anime Data**

### **3.1.1 Display Type Counts and Visualize Distribution**
"""

# Display the count of each unique value in the 'type' column
animes_type_counts = animes['type'].value_counts()
print("Anime Type Counts:")
print(animes_type_counts)

# Plot the count of each unique value in the 'type' column
plt.figure(figsize=(12, 6))
sns.countplot(x='type', data=animes, palette='PuRd')
plt.title('Distribution of Anime Types')
plt.xlabel('Anime Type')
plt.ylabel('Count')
plt.tight_layout()
plt.show()

"""1. **TV Series Dominance:**
- TV series (TV) is the most common type of anime, with 3787 instances.
- This suggests that TV series are a prevalent and popular.

2. **Diversity in Formats:**
- The dataset includes a variety of anime types, such as OVA (Original Video Animation), Movie, Special, ONA (Original Net Animation), and Music.
- The diversity in types indicates a wide range of storytelling formats and genres.

3. **Significance of OVA:**
- OVA is the second most common type, with 3311 instances.
- OVAs are often standalone episodes or series released directly to home video, indicating a significant presence of non-broadcast content.

4. **Movie Production:**
- Movies are also a substantial category, with 2348 instances.
- The presence of a large number of anime movies suggests a vibrant film industry within the anime genre.

5. **Special and Unique Productions:**
- The Special category, with 1676 instances, may include one-shot episodes, specials, or unique productions outside the standard TV series and movies.
- ONA (Original Net Animation) and Music categories are also present, indicating a diversity of content delivery methods and themes.

### **3.1.2 Display General Information and Summary Statistics**
"""

# Display general information about the 'animes' DataFrame
print("\nAnime DataFrame Info:")
print(animes[['anime_id', 'name', 'genre', 'type', 'episodes', 'rating', 'members']].info())

# Display summary statistics for the 'rating' and 'members' columns
animes_rating_members_summary = animes[['rating', 'members']].describe()
print("\nRating and Members Summary:")
print(animes_rating_members_summary)

"""1. **Data Overview:**
- The Anime DataFrame contains 12,294 entries and 7 columns.
- Columns include 'anime_id,' 'name,' 'genre,' 'type,' 'episodes,' 'rating,' and 'members.'

2. **Missing Values:**
- The 'genre' column has some missing values (62 entries).
- The 'type' column also has a few missing values (25 entries).

3. **Data Types:**
- 'anime_id' and 'members' are of type int64.
- 'rating' is of type float64.
- 'name,' 'genre,' 'type,' and 'episodes' are of type object (likely strings).

4. **Summary Statistics:**
- The 'rating' column has a count of 12,064 non-null entries, indicating some missing ratings.
- The mean rating is approximately 6.47, suggesting that, on average, anime in the dataset is well-received.
- The 'members' column represents the number of community members who have added the anime to their lists, with a mean of approximately 18,071.

5. **Rating Distribution:**
- The rating distribution ranges from a minimum of 1.67 to a maximum of 10.00.
- The majority of ratings fall within the 5.88 to 7.18 range (25th to 75th percentiles).
- This indicates a diverse range of anime with varying degrees of popularity.

6. **Members Distribution**
- The 'members' column has a wide range, with a minimum of 5 and a maximum of over 1 million.
- The distribution is positively skewed, suggesting that there are a few anime with exceptionally high member counts.

### **3.1.3 Visualize Distribution of Ratings and Members**
"""

# Visualize summary statistics for the 'rating' column
plt.figure(figsize=(10, 6))
sns.histplot(animes['rating'], bins=30, kde=True, color='pink')
plt.title('Distribution of Ratings for Animes')
plt.xlabel('Rating')
plt.ylabel('Frequency')
plt.tight_layout()
plt.show()

# Visualize summary statistics for the 'members' column
plt.figure(figsize=(10, 6))
sns.histplot(animes['members'], bins=30, kde=True, color='pink')
plt.title('Distribution of Members for Animes')
plt.xlabel('Members')
plt.ylabel('Frequency')
plt.tight_layout()
plt.show()

"""![1_zZZYdV3DNZcPkcyNyKC3Cg.png](data:image/png;base64,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)

1. **Distribution of Ratings for Animes:**
- Based on that guide, the distribution of ratings for animes is a left-skewed distribution with a longer left side of its peak than on its right.
- While the bulk of animes receive higher ratings, the presence of a left-skewed distribution suggests the existence of some animes with lower ratings.

2. **Distribution of Members for Animes**
- The distribution of members for animes shows an exponential distribution.
- This could suggest that certain shows gain popularity rapidly or decline sharply over time, rather than having a uniform or linear distribution of viewership.

### **3.1.4 Display Genre Counts and Visualize Top Genres**
"""

# Display the count of each unique value in the 'genre' column
animes_genre_counts = animes['genre'].value_counts()
print("\nAnime Genre Counts:")
print(animes_genre_counts)

# Visualize the top N genres
animes_top_genres = animes_genre_counts.head(10)
plt.figure(figsize=(12, 6))
sns.barplot(x=animes_top_genres.values, y=animes_top_genres.index, palette='PuRd')
plt.title('Top 10 Anime Genres')
plt.xlabel('Count')
plt.ylabel('Genre')
plt.tight_layout()
plt.show()

"""1. **Popularity of Genres:**
- **Hentai:** It appears to be the most popular genre based on the highest count.
- **Comedy:** Follows as the second most popular genre, with a significant number of shows.
- **Music:** Indicates a relatively high interest in anime centered around musical themes.

2. **Target Audience:**
- **Kids:** The genres "Kids" and "Fantasy, Kids" suggest a presence of content specifically designed for a younger audience.

3. **Genre Overlaps:**
- **Comedy, Slice of Life:** There is a genre overlap, indicating that comedic elements are often combined with a slice-of-life theme.
- **Fantasy, Kids:** Another instance of genre combination, suggesting fantasy content tailored for children.

4. **Niche Genres:**
- **Dementia:** This is a less common genre, indicating a niche interest in shows that may explore psychological or surreal themes.

5. **Diversity in Preferences:**
The list includes a variety of genres, reflecting the diversity of preferences among anime viewers.

### **3.1.5 Visualize Correlation Heatmap for Numerical Features**
"""

# Display a correlation heatmap for numerical features
animes_numerical_features = ['rating', 'members', 'episodes']
animes_correlation_matrix = animes[animes_numerical_features].corr()
plt.figure(figsize=(10, 8))
sns.heatmap(animes_correlation_matrix, annot=True, cmap='PuRd', fmt=".2f")
plt.title('Correlation Heatmap')
plt.tight_layout()
plt.show()

"""1. **Moderate Positive Correlation:**
- There is a positive correlation of approximately 0.39 between "rating" and "members."
- This suggests that there is a moderate tendency for anime with higher ratings to also have a larger number of members.

2. **Interdependence:**
- The positive correlation indicates that as one variable (e.g., "rating") increases, the other variable (e.g., "members") tends to increase as well, and vice versa.

3. **Viewer Engagement:**
- Anime with higher ratings might attract more members, indicating a positive relationship between audience ratings and the size of the viewership.

## **3.2 Explore Ratings Data**

### **3.2.1 Display Rating Counts and Visualize Distribution**
"""

# Display the count of each unique rating value
ratings_rating_counts = ratings.groupby("rating")["rating"].count()
print("Rating Counts:")
print(ratings_rating_counts)

# Visualize the distribution of ratings
plt.figure(figsize=(10, 6))
sns.countplot(x='rating', data=ratings, palette='PuRd')
plt.title('Distribution of Ratings')
plt.xlabel('Rating')
plt.ylabel('Count (Log Scale)')
plt.yscale('log')
plt.tight_layout()
plt.show()

"""1. **Distribution of Ratings:**
- The majority of the ratings seem to be in the higher range, with a significant number of ratings falling in the 6 to 10 range. This indicates that a substantial portion of the audience tends to rate anime positively.

2. **Popularity of Higher-Rated Anime:**
- Anime with ratings in the higher range (7 to 10) have a considerable number of ratings, indicating a popular and well-received category among the audience.

### **3.2.2 Display Total Number of Ratings and Unique User/Anime IDs**
"""

# Display the total number of ratings
ratings_total_ratings = len(ratings)
print("Total Number of Ratings:", ratings_total_ratings)

# Display the total number of unique user IDs
ratings_unique_user_ids = len(ratings['user_id'].unique())
print("\nTotal Number of Unique User IDs:", ratings_unique_user_ids)

# Display the total number of unique anime IDs
ratings_unique_anime_ids = len(ratings['anime_id'].unique())
print("\nTotal Number of Unique Anime IDs:", ratings_unique_anime_ids)

"""1. **User Engagement:**
- With 6,336,241 total ratings, there is a substantial level of user engagement on the platform. This indicates an active user base that is actively participating in rating anime.

2. **Diversity of Anime Content:**
- The presence of 9,927 unique anime IDs suggests a diverse range of anime content on the platform. This diversity could cater to a wide variety of tastes and preferences among users.

3. **User Base Size:**
- The platform has been accessed by 69,600 unique user IDs. Knowing the size of the user base is crucial for understanding the reach and impact of the platform.

### **3.2.3 Display Average Ratings per User and per Anime**
"""

# Display the average number of ratings per user
ratings_average_ratings_per_user = ratings.groupby('user_id')['rating'].count().mean()
print("Average Ratings per User:", ratings_average_ratings_per_user)

# Display the average number of ratings per anime
ratings_average_ratings_per_anime = ratings.groupby('anime_id')['rating'].count().mean()
print("\nAverage Ratings per Anime:", ratings_average_ratings_per_anime)

"""1. **Average Ratings per User (91.05):**
- The average user has given approximately 91 ratings. This suggests a moderate level of user engagement. Users are actively participating in rating anime, contributing to a diverse set of opinions.

2. **Average Ratings per Anime (638.38):**
- The average anime has received around 638 ratings. This indicates a relatively high level of attention and interest in individual anime titles. Higher average ratings per anime could suggest that a substantial number of users are watching and expressing their opinions on a wide variety of anime.

### **3.2.4 Visualize Distribution of Ratings Posted per User and per Anime**
"""

# Visualize the distribution of the number of ratings per user
ratings_per_user = ratings.groupby('user_id')['rating'].count()
plt.figure(figsize=(10, 6))
sns.histplot(ratings_per_user, bins=30, kde=True, color='pink')
plt.title('Distribution of Ratings Posted per User')
plt.xlabel('Number of Ratings per User')
plt.ylabel('Frequency')
plt.tight_layout()
plt.show()

# Visualize the distribution of the number of ratings per anime
ratings_per_anime = ratings.groupby('anime_id')['rating'].count()
plt.figure(figsize=(10, 6))
sns.histplot(ratings_per_anime, bins=30, kde=True, color='pink')
plt.title('Distribution of Ratings Posted per Anime')
plt.xlabel('Number of Ratings per Anime')
plt.ylabel('Frequency')
plt.tight_layout()
plt.show()

"""### **3.2.5 Visualize Top Users and Animes with the Most Ratings**"""

# Display the top N users with the most ratings
ratings_top_users_ratings = ratings['user_id'].value_counts().head(10)
plt.figure(figsize=(12, 6))
sns.barplot(x=ratings_top_users_ratings.index, y=ratings_top_users_ratings.values, palette='PuRd')
plt.title('Top 10 Users with the Most Ratings')
plt.xlabel('User ID')
plt.ylabel('Number of Ratings')
plt.tight_layout()
plt.show()

# Display the top N animes with the most ratings using anime names
ratings_top_animes_ratings = ratings['anime_id'].value_counts().head(10)

# Merge animes DataFrame to map anime IDs to names
top_animes_with_names = pd.merge(
    pd.DataFrame({'anime_id': ratings_top_animes_ratings.index, 'num_ratings': ratings_top_animes_ratings.values}),
    animes[['anime_id', 'name']],
    left_on='anime_id',
    right_on='anime_id'
)

plt.figure(figsize=(12, 6))
sns.barplot(x=top_animes_with_names['num_ratings'], y=top_animes_with_names['name'], palette='PuRd')
plt.title('Top 10 Animes with the Most Ratings')
plt.xlabel('Number of Ratings')
plt.ylabel('Anime Name')
plt.tight_layout()
plt.show()

# Create DataFrame for Ratings Per Anime
ratings_per_anime_df = pd.DataFrame(ratings_per_anime)
filtered_ratings_per_anime_df = ratings_per_anime_df[ratings_per_anime_df.rating >= 1000]
popular_anime_ratings = filtered_ratings_per_anime_df.index.tolist()

# Create DataFrame for Ratings Per User
ratings_per_user_df = pd.DataFrame(ratings_per_user)
filtered_ratings_per_user_df = ratings_per_user_df[ratings_per_user_df.rating <= 1000]
prolific_user_ratings = filtered_ratings_per_user_df.index.tolist()

# Filter based on both popular anime and prolific users
filtered_ratings = ratings[ratings.anime_id.isin(popular_anime_ratings) & ratings.user_id.isin(prolific_user_ratings)]

"""#### **Top 10 Users with the Most Ratings**

1. **Highly Active Users:**
- The users listed in the top 10 have significantly higher numbers of ratings compared to the general user population.
- This suggests a group of highly active and engaged users who are extensively involved in rating anime content.

2. **Potential Influencers:**
- Users with a large number of ratings may be considered influencers within the community. Their preferences might influence other users' decisions on what anime to watch, especially if they consistently rate titles in a certain way.
- Based on the plot showed, user 42635 appears to be a potential influencer on the platform. The high number of ratings (3747) suggests that this user is extensively engaged in rating anime content.
- Monitoring the preferences and ratings of user 42635 could provide valuable insights into trends and potentially influence the recommendations and decisions of other users on the platform.

#### **Top 10 Animes with the Most Ratings**

1. **Popularity Ranking:**
- The anime "Death Note" (anime_id: 1535) has the highest number of ratings (34226), indicating it is quite popular among users.

2. **Diverse Preferences:**
- The list includes a variety of genres and themes, such as "Sword Art Online" (anime_id: 11757) in the virtual reality gaming genre, "Shingeki no Kyojin" (anime_id: 16498) in the action and fantasy genre, and "Naruto" (anime_id: 20) in the shounen genre.
- This suggests that users have diverse preferences.

3. **Sequels and Franchises:**
- There are instances where multiple entries from the same franchise appear, like "Code Geass: Hangyaku no Lelouch" (anime_id: 1575) and its sequel "Code Geass: Hangyaku no Lelouch R2" (anime_id: 2904).
- This indicates that sequels and related series may also attract significant attention.

4. **Classics:**
- Anime such as "Fullmetal Alchemist: Brotherhood" (anime_id: 5114) and "Fullmetal Alchemist" (anime_id: 121) are present, suggesting that classic and highly acclaimed series continue to receive attention.

5. **Emotional Impact:**
- Titles like "Angel Beats!" (anime_id: 6547) and "Elfen Lied" (anime_id: 226) are known for their emotional impact, and their inclusion in the list may reflect users' interest in emotionally charged narratives.

### **3.2.6 User Ratings Distribution by Anime Type**
"""

# User Ratings Distribution by Anime Type
plt.figure(figsize=(12, 6))
sns.boxplot(x='type', y='rating', data=ratings.merge(animes[['anime_id', 'type']], on='anime_id'), palette='PuRd', showfliers=True)
plt.title('User Ratings Distribution by Anime Type')
plt.xlabel('Anime Type')
plt.ylabel('Rating')
plt.tight_layout()
plt.show()

"""1. **TV (Television Series):**
- The median line of the TV shows boxplot is in the middle of the box, it indicates that the median (50th percentile) rating for TV shows is around the middle of the overall range of ratings for TV shows.
- With outliers below the box, it suggests lower ratings for some TV shows.

2. **Movie:**
- The median line of the movie boxplot is in the middle of the box, it means that the median (50th percentile) rating for movies is around the middle of the overall range of ratings for movies.
- Few outliers suggest some movies received exceptionally low ratings.

3. **Special:**
- The median line of the special boxplot is in the middle of the box, it means that the median (50th percentile) rating for special is around the middle of the overall range of ratings for special.
- Few outliers suggest some special received exceptionally low ratings.

4. **OVA (Original Video Animation):**
- The box is wide, indicating variability.
- The median line is lower compared to other, suggesting a lower median rating.
- Outliers suggest some OVAs received very low ratings.

5. **ONA (Original Net Animation) and Music:**
- The boxes for "ONA" and "Music" are positioned in the lower whiskers, it indicates that the majority of the ratings for these anime types are concentrated in the lower range.
- The median line is positioned in the middle of the box.

# **4. Recommendation System**

## **4.1 Data Preparation and Matrix Creation**
"""

rating_matrix = filtered_ratings.pivot_table(index='user_id', columns='anime_id', values='rating')
rating_matrix = rating_matrix.fillna(0)
rating_matrix.head()

"""## **4.2 Similar User Identification**"""

def similar_users(user_id, matrix, k=5):

    # Find similar users to the given user based on cosine similarity.

    # Parameters:
    # - user_id (int): The target user ID.
    # - matrix (pd.DataFrame): The rating matrix.
    # - k (int): Number of similar users to retrieve.

    # Returns:
    # - List of similar user indices.
    # - List of (user_index, cosine_similarity_score) tuples.

    # Check if the user has any ratings
    if user_id not in matrix.index:
        print(f"User {user_id} has no ratings.")
        return [], []

    user = matrix.loc[matrix.index == user_id]
    other_users = matrix.loc[matrix.index != user_id]

    # Check if the other_users DataFrame is not empty
    if other_users.empty:
        print("No other users with ratings.")
        return [], []

    similarities = cosine_similarity(user, other_users)[0].tolist()
    indices = other_users.index.tolist()
    index_similarity = dict(zip(indices, similarities))
    index_similarity_sorted = sorted(index_similarity.items(), key=operator.itemgetter(1), reverse=True)
    top_users_similarities = index_similarity_sorted[:k]
    users = [u[0] for u in top_users_similarities]

    return users, top_users_similarities

"""## **4.3 Recommendation Function Definition**"""

def recommend_item(user_index, similar_user_indices, matrix, items=5, anime_data=None):

    # Generate item recommendations for a given user based on similar users' ratings.

    # Parameters:
    # - user_index (int): Index of the target user.
    # - similar_user_indices (list): List of indices of similar users.
    # - matrix (pd.DataFrame): The rating matrix.
    # - items (int): Number of items to recommend.

    # Returns:
    # - pd.Series: Series containing mean ratings of similar users for unseen items.
    # - list: List of top N recommended item indices.

   # Get ratings of similar users
    similar_users = matrix[matrix.index.isin(similar_user_indices)]
    similar_users_mean = similar_users.mean(axis=0)

    # Ensure the user_index is converted to integer (if needed)
    user_index = int(user_index)

    # Filter ratings of unseen animes from similar users directly in the mean calculation
    similar_users_ratings = similar_users_mean[similar_users_mean.index.isin(matrix.loc[user_index][matrix.loc[user_index] == 0].index)]

    # Sort by mean rating in descending order
    similar_users_ratings_sorted = similar_users_ratings.sort_values(ascending=False)

    # Get top N recommendations
    top_n_anime_indices = similar_users_ratings_sorted.head(items).index.tolist()

    # If anime_data is provided, add anime names to the recommendations
    if anime_data is not None:
        recommendations_with_names = pd.merge(
            pd.DataFrame({'mean_rating': similar_users_ratings_sorted}),
            anime_data[['anime_id', 'name']],
            left_index=True,
            right_on='anime_id'
        )
        return recommendations_with_names, top_n_anime_indices
    else:
        return similar_users_ratings_sorted, top_n_anime_indices

"""## **4.4 Recommendation Function Definition (Specifically for 'Movie' Anime Type)**"""

def recommend_movie(user_index, similar_user_indices, matrix, items=5, anime_data=None):
    # Generate item recommendations for a given user based on similar users' ratings.

    # Parameters:
    # - user_index (int): Index of the target user.
    # - similar_user_indices (list): List of indices of similar users.
    # - matrix (pd.DataFrame): The rating matrix.
    # - items (int): Number of items to recommend.
    # - anime_data (pd.DataFrame): Dataframe containing anime information.

    # Returns:
    # - pd.DataFrame: DataFrame containing mean ratings of similar users for unseen 'Movie' items with names.
    # - list: List of top N recommended 'Movie' item indices.

    # Get ratings of similar users
    similar_users = matrix[matrix.index.isin(similar_user_indices)]
    similar_users_mean = similar_users.mean(axis=0)

    # Ensure the user_index is converted to integer (if needed)
    user_index = int(user_index)

    # Filter ratings of unseen 'Movie' animes from similar users directly in the mean calculation
    unseen_movies = matrix.loc[user_index][matrix.loc[user_index] == 0].index
    similar_users_ratings = similar_users_mean[unseen_movies]

    # Sort by mean rating in descending order
    similar_users_ratings_sorted = similar_users_ratings.sort_values(ascending=False)

    # Get top N recommendations
    top_n_movie_indices = similar_users_ratings_sorted.head(items).index.tolist()

    # If anime_data is provided, add 'Movie' names to the recommendations
    if anime_data is not None:
        recommendations_with_names = pd.merge(
            pd.DataFrame({'mean_rating': similar_users_ratings_sorted}),
            anime_data[['anime_id', 'name', 'type']],
            left_index=True,
            right_on='anime_id'
        )
        recommendations_movies = recommendations_with_names[recommendations_with_names['type'] == 'Movie']
        return recommendations_movies, top_n_movie_indices
    else:
        return similar_users_ratings_sorted, top_n_movie_indices

"""## **4.5 Specific Recommendations for User ID 226**

### **4.5.1 Similar Users to User ID 226**
"""

user_id = 226
similar_user_indices, top_users_similarities = similar_users(user_id, rating_matrix)

# Visualization
plt.figure(figsize=(12, 6))
sns.barplot(x=[user[0] for user in top_users_similarities], y=[user[1] for user in top_users_similarities], palette='PuRd')
plt.title(f'Top {len(top_users_similarities)} Users Similar to User {user_id}')
plt.xlabel('User ID')
plt.ylabel('Cosine Similarity Score')
plt.tight_layout()
plt.show()

"""1. **User IDs of Similar Users:**
- 40763
- 22642
- 47744
- 39021
- 17479

2. **Similarity Scores:**
- 0.681 for user 40763
- 0.678 for user 22642
- 0.674 for user 47744
- 0.673 for user 39021
- 0.669 for user 17479

### **4.5.2 Recommendations for User ID 226**
"""

user_index = 226
similar_user_indices, _ = similar_users(user_index, rating_matrix)
recommendations, top_recommendations_indices = recommend_item(user_index, similar_user_indices, rating_matrix, anime_data=animes)

# Plotting the top 5 recommendations with anime names and text annotations
plt.figure(figsize=(12, 6))
barplot = sns.barplot(x=recommendations['mean_rating'].head(5).values, y=recommendations['name'].head(5), palette='PuRd')

# Add text annotations to each bar
for index, value in enumerate(recommendations['mean_rating'].head(5).values):
    barplot.text(value, index, f'{value:.2f}', color='black', ha="left", va="center")

plt.title(f'Top 5 Recommendations for User {user_index}')
plt.xlabel('Mean Rating')
plt.ylabel('Anime Name')
plt.show()

"""1. **"Gate: Jieitai Kanochi nite, Kaku Tatakaeri" (Anime ID: 28907):**
- This anime has a mean rating of approximately 8.33 based on the ratings of users similar to user ID 226.
- It seems to be highly rated by these similar users, suggesting that it might align well with the preferences of user 226.

2. **"Shokugeki no Souma" (Anime ID: 28171):**
- This anime has a mean rating of 8.00 among similar users.
- It's also highly rated, indicating that it could be a good recommendation for user 226.

3. **"Toaru Majutsu no Index II" (Anime ID: 8937):**
- Similar to the previous two, this anime has a mean rating of 7.80 among users similar to user 226.
- It's another potentially suitable recommendation.

4. **"Btooom!" (Anime ID: 14345):**
- This anime has a slightly lower mean rating of 7.67 among similar users.
- While still a decent rating, it might be considered a bit less preferred compared to the others.

5. **"Kill la Kill" (Anime ID: 18679):**
- With a mean rating of 7.67, this anime is similar in rating to "Btooom!" among users similar to user 226.

### **4.5.3 Recommendations for User ID 226 (Specifically for 'Movie' Anime Type)**
"""

user_index = 226
similar_user_indices, _ = similar_users(user_index, rating_matrix)
recommendations, top_recommendations_indices = recommend_movie(user_index, similar_user_indices, rating_matrix, anime_data=animes)

# Plotting the top 5 recommendations with 'Movie' names and text annotations
plt.figure(figsize=(12, 6))
barplot = sns.barplot(x=recommendations['mean_rating'].head(5).values, y=recommendations['name'].head(5), palette='PuRd')

# Add text annotations to each bar
for index, value in enumerate(recommendations['mean_rating'].head(5).values):
    barplot.text(value, index, f'{value:.2f}', color='black', ha="left", va="center")

plt.title(f'Top 5 Movie Recommendations for User {user_index}')
plt.xlabel('Mean Rating')
plt.ylabel('Movie Name')
plt.show()

"""1. **Bleach Movie 3: Fade to Black - Kimi no Na wo Yobu:**
- Mean Rating: 4.0
- This movie has received a high mean rating of 4.0, indicating that users similar to user 226 have rated it positively.

2. **Bleach Movie 1: Memories of Nobody:**
- Mean Rating: 4.0
- Similar to the first movie, this one also has a mean rating of 4.0, suggesting a positive reception among users with similar preferences.

3. **Bleach Movie 2: The DiamondDust Rebellion - Mou Hitotsu no Hyourinmaru:**
- Mean Rating: 4.0
- The second Bleach movie also has a high mean rating of 4.0, showing consistent positive feedback from users.

4. **Break Blade 1: Kakusei no Toki:**
- Mean Rating: 3.8
- While slightly lower than the Bleach movies, this movie still has a respectable mean rating of 3.8, indicating favorable reviews.

5. **Sora no Otoshimono: Tokeijikake no Angeloid:**
- Mean Rating: 3.4
- This movie has a mean rating of 3.4, which is the lowest among the top 5 recommendations. It might still be a decent choice, but users may have varied opinions.
"""
