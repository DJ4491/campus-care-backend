# Placeholder: we will call rec_engine here
from app.services.rec_engine import simple_mutual_rec, simple_page_rec
# from app.services.firebase_service import firestore
from app.services.firebase_service import db

def get_mutual_friend_recommendations_for_user(user_id):

    try:
        data = {}
        response = (
            service_supabase.table("profiles")
            .select("id, created_at, username")
            .order("created_at", desc=True)
            .execute()
        )

        friendship_response = (
            service_supabase.table("friendships")
            .select("user_id,friend_id")
            .eq("status", "accepted")
            .execute()
        )
        friendship_data = friendship_response.data
        data["users"] = response.data

        for user in data["users"]:
            if "friends" not in user:
                user["friends"] = []
            for friend in friendship_data:
                if user["id"] == friend["user_id"]:
                    user["friends"].append(friend["friend_id"])

        return simple_mutual_rec(user_id, data)
        # return data
    except Exception as e:
        return f"There was a problem: {e}"


def get_posts_recommendations_for_user(user_id):

    try:

        data = {}
        response = (
            service_supabase.table("profiles")
            .select("id,created_at,username")
            .order("created_at", desc=True)
            .execute()
        )

        likes_response = (
            service_supabase.table("likes").select("user_id,post_id").execute()
        )

        posts_response = (
            service_supabase.table("posts").select("id,author_id").execute()
        )

        post_author_map = {}

        for post in posts_response.data:
            post_id = post["id"]
            author_id = post["author_id"]
            post_author_map[post_id] = author_id

        created_by_user = set()

        for p_id, auth_id in post_author_map.items():
            if auth_id == user_id:
                created_by_user.add(p_id)

        data["created_by_user"] = created_by_user

        likes_data = likes_response.data or []
        data["users"] = response.data or []

        for user in data["users"]:
            if "liked_posts" not in user:
                user["liked_posts"] = []

            for post in likes_data:
                if user["id"] == post["user_id"]:
                    user["liked_posts"].append(post["post_id"])

        return simple_page_rec(user_id, data)
    except Exception as e:
        return f"There was a problem: {e}"
