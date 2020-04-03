from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
auth_url = gauth.GetAuthUrl()

gauth.LoadCredentialsFile("creds.json")
if gauth.credentials is None:
    print("Please, run the sho2.py script.")
    exit()
elif gauth.access_token_expired:
    gauth.Refresh()
else:
    gauth.Authorize()

gauth.SaveCredentialsFile("creds.json")

drive = GoogleDrive(gauth)
