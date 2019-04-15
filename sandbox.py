from linkedin_api import Linkedin

# Authenticate using any Linkedin account credentials
api = Linkedin('pipexir@gmail.com', 'pipuchis10')

# GET a profile
profile = api.searchTotal({
    'keywords':'java', 
    'location': 'Estados Unidos', 
    'locationId': 'us:0', 
    'type': 'JOBS', 'query': 'search',
})


print(profile)
