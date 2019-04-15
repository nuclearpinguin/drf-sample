from movies.models import Comment
from collections import Counter
from requests import get
from datetime import datetime
from django.utils.timezone import make_aware


def top_counter(date_from: str, date_to: str) -> list:
    """
    Creates movies ranking based on the number of comments created
    in given date range.

    Default range is the last week.

    Parameters
    ----------
    date_from - string representing lower bound for date range ex. '2019-03-19'
    date_to - string representing upper bound for date range

    """
    date_from = make_aware(datetime.strptime(date_from, "%Y-%m-%d"))
    date_to = make_aware(datetime.strptime(date_to, "%Y-%m-%d"))

    comments = Comment.objects.filter(
        created__range=(date_from, date_to)
    )

    # Make counter on move ids
    counter = Counter([c.movie_id for c in comments])

    # Find unique numbers of comments
    unique_counts = list(set(counter.values()))
    unique_counts.sort(reverse=True)

    # Create ranking based on number of comments
    rank_map = {v: i+1 for i, v in enumerate(unique_counts)}

    # Create ranking list
    rank_list = [{'movie_id': k.id, "rank": rank_map[v], "total_comment": v} for k, v in counter.items()]

    return rank_list


def omdb_enrichment(title: str) -> tuple:
    """
    Fetches additional information from OMDb API.

    Parameters
    ----------
    title - movie title

    """
    response = get(f"http://www.omdbapi.com/?apikey=cbf4722f&t={title}")

    if response.status_code != 200:
        return None, None, None

    body = response.json()

    return body.get("Genre"), body.get("Director"), body.get("Metascore")
