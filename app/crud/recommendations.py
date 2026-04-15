# Placeholder: we will call rec_engine here
from app.services.rec_engine import simple_mutual_rec, simple_page_rec

# from app.services.firebase_service import firestore
from app.services.firebase_service import db
from firebase_admin import firestore

# def get_mutual_friend_recommendations_for_user(user_id):

#     try:
#         data = {}
#         response = db.collection("posts").order_by('created_at',direction = firestore.Query.DESCENDING)

#         friendship_response = (
#             service_supabase.table("friendships")
#             .select("user_id,friend_id")
#             .eq("status", "accepted")
#             .execute()
#         )
#         friendship_data = friendship_response.data
#         data["users"] = response.data

#         for user in data["users"]:
#             if "friends" not in user:
#                 user["friends"] = []
#             for friend in friendship_data:
#                 if user["id"] == friend["user_id"]:
#                     user["friends"].append(friend["friend_id"])

#         return simple_mutual_rec(user_id, data)
#         # return data
#     except Exception as e:
#         return f"There was a problem: {e}"


def get_posts_recommendations_for_user(user_id):

    try:

        data = {}
        response = (
            db.collection("profiles")
            .select(["id", "createdAt", "name"])
            .order_by("createdAt", direction=firestore.Query.DESCENDING)
        )
        
        profile_docs = response.stream()
        
        likes_response = db.collection("likes").select(["postId", "userId"])
         
        likes_docs = likes_response.stream()    

        posts_response = (
            db.collection("posts")
            .select(["created_at", "title","author.id"])
            .order_by("created_at", direction=firestore.Query.DESCENDING)
        )

        docs = posts_response.stream()

        posts_data = []
        for doc in docs:
            post_data = doc.to_dict()
            post_data["id"] = doc.id
            posts_data.append(post_data)
        
        users = []
        for doc in profile_docs:
            user_data = doc.to_dict()
            user_data["id"] = doc.id
            users.append(user_data)
        
        likes = []
        for doc in likes_docs:
            like_data = doc.to_dict()
            likes.append(like_data)
        
        
        post_author_map = {}

        for post in posts_data:
            post_id = post["id"]
            author_id = post.get('author',{}).get('id')
            post_author_map[post_id] = author_id

        created_by_user = set()

        for p_id, auth_id in post_author_map.items():
            if auth_id == user_id:
                created_by_user.add(p_id)

        data["created_by_user"] = created_by_user

        likes_data = likes or []
        data["users"] = users or []

        for user in data["users"]:
            if "liked_posts" not in user:
                user["liked_posts"] = []

            for post in likes_data:
                if user["id"] == post["userId"]:
                    user["liked_posts"].append(post["postId"])

        return simple_page_rec(user_id, data)
    except Exception as e:
        return f"There was a problem: {e}"
