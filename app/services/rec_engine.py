# A tiny placeholder recommendation engine
from collections import Counter
import heapq


def simple_mutual_rec(user_id: str, data, limit: int = 10):  # API consumer can request how many recommendations they want
    if not isinstance(data, dict) or "users" not in data:
        raise ValueError("Invalid data format: expected {'users': [...]}")
    # TODO: fetch follow relations from Supabase and compute mutual counts
    user_friends = {}  # Lookup Dictionary
    for user in data["users"]:
        user_friends[user["id"]] = set(user["friends"])

    if user_id not in user_friends:
        raise KeyError("User not found")

    direct_friends = user_friends[user_id]
    suggestions = Counter()
    for friend in direct_friends:

        if friend not in user_friends:
            continue

        for mutual in user_friends[friend]:  # Friends Of Friend

            if mutual not in user_friends:
                continue

            if mutual == user_id or mutual in direct_friends:
                continue

            suggestions[mutual] += 1
    # Take all suggested users, sort them by number of mutual friends, highest first
    top_pairs = heapq.nlargest(limit, suggestions.items(), key=lambda x: x[1])
    return [user_id for user_id, mutual_count in top_pairs]


def simple_page_rec(user_id: str, data, limit: int = 10):
    # Structuring the Data in a new list with users id and liked_pages
    if not isinstance(data, dict) or "users" not in data:
        raise ValueError("Invalid data format: expected {'users': [...]}")
    
    user_Posts = {}
    for user in data["users"]:
        user_Posts[user["id"]] = set(user["liked_posts"])

    # Checking if the user is in user_pages or not
    if user_id not in user_Posts:
        raise KeyError("User not found")

    # Creating a new set that groups the user's liked pages in ids
    user_liked_posts = user_Posts[user_id]
    page_suggestions = Counter()  # Score based on which the recommendation system will work
    
    created_by_user = data.get("created_by_user",set())

    # Looping through the user_Posts's items i.e other_user_id and thier liked pages ( BOTH KEY AND VALUE )
    for other_user_id, posts in user_Posts.items():
        # Checking if other_user_id is not the currect user_id which we are gonna recommend the pages
        if other_user_id != user_id:
            shared_posts = user_liked_posts.intersection(posts)  # Finding out the common liked pages btw the other user and the current user
        # Looping through each page of the other user's liked pages
            for post in posts:
                # Checking if the page is not already a liked page by the current user
                if post in user_liked_posts:
                    continue
                if post in created_by_user:
                    continue
                # Page id : score
                page_suggestions[post] += len(shared_posts)
        # Good'ol sorting
    # sorted_posts = sorted(page_suggestions.items(), key=lambda x: x[1], reverse=True)
    sorted_posts = heapq.nlargest(limit,page_suggestions.items(), key=lambda x: x[1])
        # Returning the page_id that needs to be recommended
    return [page_id for page_id, score in sorted_posts]