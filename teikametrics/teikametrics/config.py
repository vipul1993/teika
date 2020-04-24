import os

if 'teika_client_id' in os.environ and os.environ.get('teika_client_id') != 'your_client_id':
	pass
else:
	os.environ["teika_client_id"] = "64038e2b0280c85fcccf"

if 'teika_client_secret' in os.environ and os.environ.get('teika_client_secret') != 'your_client_secret':
	pass
else:
	os.environ["teika_client_secret"] = "4baf8b6bad6c028a2c8e0ced3d8cb90f5fb10727"

if 'teika_access_token' in os.environ:
	pass
else:
	os.environ["teika_access_token"] = ''				