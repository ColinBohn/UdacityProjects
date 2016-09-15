import media
import fresh_tomatoes

# Begin creating objects for movies we wish to display

# Zootopia
zootopia = media.Movie("Zootopia",
                       "A rabbit works to solve a mysterious case with a fox.",
                       "https://lumiere-a.akamaihd.net/v1/images/"
                       "movie_poster_zootopia_866a1bf2.jpeg",
                       "https://www.youtube.com/watch?v=jWM0ct-OLsM")

# Ghostbusters
ghostbusters = media.Movie("Ghostbusters",
                           "Professional ghost exterminators save the"
                           "city from paranormal happenings.",
                           "https://upload.wikimedia.org/wikipedia/en/2/2f/"
                           "Ghostbusters_%281984%29_theatrical_poster.png",
                           "https://www.youtube.com/watch?v=vntAEVjPBzQ")

# Patema Inverted
patema = media.Movie("Patema Inverted",
                     "A boy and girl from above and below the surface"
                     " uncover the secrets of their opposite gravity.",
                     "https://upload.wikimedia.org/wikipedia/"
                     "en/5/5f/Patema_Inverted_DVD.jpg",
                     "https://www.youtube.com/watch?v=Aa7sa-Zd-3E")

# Little Witch Academia
academia = media.Movie("Little Witch Academia",
                       "A girl enrolls into a magical academy after"
                       " being inspired by a performing witch.",
                       "https://upload.wikimedia.org/wikipedia/"
                       "en/7/73/Littlewitchacademiacover.jpeg",
                       "https://www.youtube.com/watch?v=oOWIqupLzb0")

# Combine movies into a list
movies = [zootopia, ghostbusters, patema, academia]

# Render list into an HTML file, and open the page
fresh_tomatoes.open_movies_page(movies)
