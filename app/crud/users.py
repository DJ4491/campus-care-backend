# from app.services.firebase_service import service_supabase


# def get_user_by_id(user_id: str):
#     res = service_supabase.table("profiles").select("*").eq("id", user_id).execute()
#     return res.data if res.data else None
