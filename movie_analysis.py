import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# csv
basics = pd.read_csv(
    "title.basics.csv",
    names=["tconst","titleType","primaryTitle","originalTitle","isAdult","startYear","endYear","runtimeMinutes","genres"],
    header=None,
    low_memory=False
)
ratings = pd.read_csv(
    "title.ratings.csv",
    names=["tconst","averageRating","numVotes"],
    header=None,
    low_memory=False
)

# 2. data filtering (movie only)
movies = basics[basics["titleType"] == "movie"]

# 3. merge
df = pd.merge(movies, ratings, on="tconst", how="inner")

df = df[(df["startYear"] != "\\N") & (df["genres"] != "\\N")]
df["startYear"] = pd.to_numeric(df["startYear"], errors='coerce')
df = df.dropna(subset=["startYear"])  
df["startYear"] = df["startYear"].astype(int)

# genre
df["main_genre"] = df["genres"].str.split(",").str[0]

# numvotes, averagerating to numeric
df["numVotes"] = pd.to_numeric(df["numVotes"], errors='coerce')
df["averageRating"] = pd.to_numeric(df["averageRating"], errors='coerce')
df = df.dropna(subset=["numVotes", "averageRating"]) 

# filtering votes
df = df[df["numVotes"] > 100]

print("data:", df.shape)
print(df.head())

# -------------------------------
# analyzing
# -------------------------------

# 1) genre average rating
genre_rating = df.groupby("main_genre")["averageRating"].mean().sort_values(ascending=False)

plt.figure(figsize=(12,6))
sns.barplot(x=genre_rating.index, y=genre_rating.values, hue=genre_rating.index, palette="viridis", legend=False)
plt.xticks(rotation=45)
plt.title("Average Rating by Genre (IMDb Movies)")
plt.ylabel("Average Rating")
plt.tight_layout()
plt.show()

# 2) top 10 movie after 2000
top10_movies = (
    df[(df["startYear"] >= 2000) & (df["numVotes"] > 10000)]
    .sort_values(by="averageRating", ascending=False)
    .head(10)[["primaryTitle", "startYear", "averageRating", "numVotes", "main_genre"]]
)

print("\n🎬 IMDB Top 10 movie after 2000:")
print(top10_movies.to_string(index=False))

# graph visualiztion
plt.figure(figsize=(12,6))
plt.barh(top10_movies["primaryTitle"], top10_movies["averageRating"], color="skyblue")
plt.gca().invert_yaxis()  
plt.title("Top 10 Movies since 2000 (by IMDb Rating)")
plt.xlabel("Average Rating")
plt.ylabel("Movie Title")
plt.tight_layout()
plt.show()

# 3) runtime vs average rating
df["runtimeMinutes"] = pd.to_numeric(df["runtimeMinutes"], errors="coerce")
df_runtime = df.dropna(subset=["runtimeMinutes"])

plt.figure(figsize=(10,6))
sns.scatterplot(data=df_runtime, x="runtimeMinutes", y="averageRating", alpha=0.3)
plt.title("Runtime vs Average Rating")
plt.xlabel("Runtime (minutes)")
plt.ylabel("Average Rating")
plt.xlim(0, 300) 
plt.tight_layout()
plt.show()

# 4) top 1 movie by votes in each genre
top_votes_by_genre = (
    df.sort_values("numVotes", ascending=False)
    .groupby("main_genre")
    .head(1)[["main_genre", "primaryTitle", "numVotes", "averageRating"]]
)

print("\n🎬 Top movie by votes in each genre:")
print(top_votes_by_genre.to_string(index=False))

#graph
plt.figure(figsize=(12,6))
sns.barplot(
    data=top_votes_by_genre,
    x="numVotes", y="primaryTitle", hue="main_genre", dodge=False, legend=False
)
plt.title("Most Voted Movie by Genre")
plt.xlabel("Number of Votes")
plt.ylabel("Movie Title")
plt.tight_layout()
plt.show()

# 5) votes vs average rating
plt.figure(figsize=(10,6))
sns.scatterplot(data=df, x="numVotes", y="averageRating", alpha=0.3)
plt.xscale("log") 
plt.title("Votes vs Average Rating")
plt.xlabel("Number of Votes (log scale)")
plt.ylabel("Average Rating")
plt.tight_layout()
plt.show()
