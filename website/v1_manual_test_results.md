# Example workflow
As someone who is curious about their consumption, I want to be able to log my meals so I can view them whenever I want

# Testing results
<Repeated for each step of the workflow>
1. The curl statement called. You can find this in the /docs site for your 
API under each endpoint. For example, for my site the /catalogs/ endpoint 
curl call looks like:
curl -X 'GET' \
  'https://centralcoastcauldrons.vercel.app/catalog/' \
  -H 'accept: application/json'

ADD MEAL 1
ADD MEAL 2
GET ALL MEALS
2. The response you received in executing the curl statement.
RESPONSE JSON FROM THESE 3