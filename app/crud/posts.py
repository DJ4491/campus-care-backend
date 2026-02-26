# app/crud/posts.py
import logging

from firebase_admin import firestore
from app.services.firebase_service import db

# This logger is configured in app/main.py, so it's ready to use.
logger = logging.getLogger(__name__)    


def create_post_db(limit: int, cursor: str | None = None):
    logger.info(f"Received request for posts: limit={limit}, cursor='{cursor}'")

    # Base query: newest first
    query = db.collection("posts").order_by("created_at", direction=firestore.Query.DESCENDING)
    logger.debug("Base query created with order_by('created_at', DESCENDING)") # Use debug for very granular info
    cursor = cursor.strip()
    cursor = cursor.strip('"')
    # If cursor exists, fetch the document snapshot and anchor after it
    if cursor:  
        cursor_doc_ref = db.collection("posts").document(cursor)
        # Note: .get() is also synchronous
        cursor_doc = cursor_doc_ref.get()
        logger.info(f"Cursor document '{cursor}' exists: {cursor_doc.exists}")
        if cursor_doc.exists:
            query = query.start_after(cursor_doc)
            logger.debug("start_after applied to query.")
        else:
            logger.warning(f"Cursor document '{cursor}' does not exist. Query will proceed without start_after, potentially returning the first page.")
            # Optional: You could decide that an invalid cursor means no results
            # return {"posts": [], "nextCursor": None}

    # Apply limit
    query = query.limit(limit)
    logger.debug(f"Limit of {limit} applied to query.")

    # Execute query
    posts = []
    last_doc_id = None
    doc_count_in_result = 0 # Counter for documents actually retrieved

    try:
        logger.info("Attempting to stream documents from Firestore...")
        # query.stream() is synchronous, no 'await' needed here
        docs = query.stream() 
        
        for doc in docs:
            doc_count_in_result += 1
            data = doc.to_dict()
            data["id"] = doc.id
            posts.append(data)
            last_doc_id = doc.id
            logger.debug(f"Added document: {doc.id} with data: {data}") # Log each doc for very detailed debugging

        logger.info(f"Successfully retrieved {doc_count_in_result} documents from Firestore.")
        if not posts:
            logger.info("Firestore query returned an empty set of documents after streaming.")

    except Exception as e:
        logger.error(f"FATAL Firestore query error in create_post_db: {e}", exc_info=True)
        # exc_info=True will print the full traceback, which is crucial for debugging
        return {"posts": [], "nextCursor": None, "error": "Firestore query error. Check backend logs for details."}

    logger.info(f"Returning {len(posts)} posts. Next cursor: {last_doc_id}")
    return {"posts": posts, "nextCursor": last_doc_id}

