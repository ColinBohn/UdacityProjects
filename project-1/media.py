class Movie():
    '''This class provides storage for details about a movie'''
    def __init__(self, title, summary, imageUrl, trailerUrl):
        self.title = title
        self.storyline = summary
        self.poster_image_url = imageUrl
        self.trailer_youtube_url = trailerUrl
