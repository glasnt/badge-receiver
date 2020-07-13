deploy: 
	gcloud builds submit

local: 
	python app.py

post_test:
	curl -H "Content-Type: application/json" -d '{"status": "SUCCESS", "substitutions": {"_SERVICE": "curl-test", "COMMIT_SHA": "1234abc"}}' http://localhost:8080/receive

get_test:
	open http://localhost:8080/service/curl-test/badge.svg 
