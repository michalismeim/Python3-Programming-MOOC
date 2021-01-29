#reference: https://github.com/RichardDanielOliva/PythonDataCollectionAndProcessingCourseProject/blob/master/course3ProjectDataCollection.py

# please review again and retry


import requests_with_caching
import json

def get_movies_from_tastedive(name):
    baseurl = "https://tastedive.com/api/similar"
    parm = {}
    parm["q"] = name
    parm["type"] = "movies"
    parm["limit"] = 5
    resp = requests_with_caching.get(baseurl, params = parm)
    print(resp.url)
    return resp.json()

def extract_movie_titles(movies_list):
    movies = []
    for m in movies_list['Similar']['Results']:
        movies.append(m['Name'])
    print(movies)
    return movies

def get_related_titles(titles_list):
    if titles_list != []:
        auxList=[]
        relatedList=[]
        for movieName in titles_list:
            auxList = extract_movie_titles(get_movies_from_tastedive(movieName))
            for movieNameAux in auxList:
                if movieNameAux not in relatedList:
                    relatedList.append(movieNameAux)
        return relatedList
    return titles_list
    
    
def get_movie_data(movie):
    url = 'http://www.omdbapi.com/'
    param = {}
    param['t'] = movie
    param['r'] = 'json'
    response = requests_with_caching.get(url, params = param)
    return response.json()
    
    
def get_movie_rating(movieName):
    strRating=""
    for typeRatingList in movieName["Ratings"]:
        if typeRatingList["Source"]== "Rotten Tomatoes":
            strRating = typeRatingList["Value"]
    if strRating != "":
        rating = int(strRating[:2])
    else: rating = 0
    return rating
    
    
def get_sorted_recommendations(m_titles):
    listMovie= get_related_titles(m_titles)
    listMovie= sorted(listMovie, key = lambda movieName: (get_movie_rating(get_movie_data(movieName)), movieName), reverse=True)
    
    return listMovie

# some invocations that we use in the automated tests; uncomment these if you are getting errors and want better error messages
get_movies_from_tastedive("Bridesmaids")
#get_movies_from_tastedive("Black Panther")


