# drf-sample

## Setup

Just make 

```
docker-compose up
```

## Enpoints 

`POST api/movies`✅

Request body should contain only movie title:
```json
{"title": "Lord of the Rings"}
```
Based on passed title, other movie details are fetched from OMDb.
Response includes full movie object, along with all fetched data.

`GET api/movies` ✅

Fetch list of all movies already present in application database.

```json
[
  {
    "id": 1,
    "title": "Harry Potter and the Deathly Hallows",
    "director": "David Yates",
    "genre": "Adventure, Drama, Fantasy, Mystery",
    "metascore": 87
  },
  {
    "id": 2,
    "title": "Lord of the Rings",
    "director": "Peter Jackson",
    "genre": "Adventure, Drama, Fantasy",
    "metascore": 92
  }
  ...
]
```

Movies could be filtered by metascore. By passing query param `metascore=76` 
you get a list of movies with metascore greater or equal to 76.

`POST api/comments:` ✅

Request body should contain ID of movie already present in database, and comment text body.

```json
{"body": "Very interesting movie", "movie_id": 12}
```
In response one gets the comment with its unique id.

`GET api/comments`✅
​
Fetch list of all comments present in application database.

```json

[
  {
    "id": 1,
    "body": "Some interesting comment",
    "movie_id": 1
  },
  {
    "id": 2,
    "body": "Another meaningful comment",
    "movie_id": 1
  },
  ...
]
```

`GET api/comments/<movie_id>`✅

Fetch list of all comments for a given movie id.

`GET /top`

Returns top movies already present in the database ranking based on a number of comments added to the movie.
If there are no comments then there is no ranking.

```json
[
  {
    "movie_id": 1,
    "rank": 1,
    "total_comment": 3
  },
  {
    "movie_id": 2,
    "rank": 1,
    "total_comment": 3
  }
]
```

One can specify date range for the ranking using body:

```json
{
  "date_from": "2019-01-07", 
  "date_to": "2019-04-20"
 }
```

Default range is last 7 days from today.
