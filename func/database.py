import firebase_admin
from firebase_admin import credentials, firestore

cred = firebase_admin.credentials.Certificate(
		'serviceAccountKey.json')
fireApp = firebase_admin.initialize_app(cred)
dbClient = firebase_admin.firestore.client()
dbUser = dbClient.collection("users")

def update_data(userid, platform, username):
    try:
        user_doc_ref = dbUser.document(userid)
        user_doc_ref.set({
                'platforms': {
                    platform: username
                }
            }, merge=True)
    except Exception as e:
        print(e)

def remove_data(userid, platform):
    try:
        user_doc_ref = dbUser.document(userid)
        user_doc_ref.update({
            f'platforms.{platform}': firestore.DELETE_FIELD
        })
    except Exception as e:
        print(e)

def query_data(userid):
    try:
        user_doc_ref = dbUser.document(userid)
        doc = user_doc_ref.get()
        
        if doc.exists:
            user_data = doc.to_dict()
            platforms = user_data.get('platforms', {})
            return platforms
        else:
            return {}
    except Exception as e:
        print(e)
        return {}


# remove_data("1","cf")
# update_data("1","cf","tkt0506tkt")
# print(query_data("1"))

# add data : !update [platform] [username]
# remove data : !remove [platform]
# 