## Fast API 

### Dockerfile
command to create the dockerfile:
```
docker build -t recom-sys .   
```
Then to run the dockerfile:
```
docker run -p 8000:80  recom-sys 
```

Need to get the date and time for the events but not going to scrape so no need.

Remember before creating new dockerfile need to add the new libraries from pip and venv into requirements.txt


