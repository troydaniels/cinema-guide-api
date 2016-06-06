# cinema-guide-api

####A small API to allow access to cinema guide listings, utilizing the Django REST Framework

This API supports the application/json media type, with all valid GET queries returning a JSON object.

A series of tests for this API can be found under `cinema-guide-api/project/cinema_guide_api/test*`, and can be run using `python manage.py test`

####Available operations:
####/cinema/
Allows: GET, POST

Lists all cinemas, or allows the creation of a new cinema

####/movie/
Allows: GET, POST

Lists all movies, or allows the creation of a new movie

####/cinema/{identifier}
Allows: GET, PUT, DELETE

Lists cinema-specific information, for a non-case sensitive cinema name or id number. Also allows for editing or deletion of these records.
Note: The string "suburb" (case insensitive) is reserved, and should not be used as a cinema name

####/movies/{identifier}
Allows: GET, PUT, DELETE

Lists movie-specific information, for a non-case sensitive movie name or id number. Also allows for editing or deletion of these records.

####/cinema/{identifier}/{date}
Allows: GET

Retrieves movies playing at a given cinema, specified by a non-case sensitive cinema name or id number, on a given date, in the format YYYY-MM-DD

####/cinema/{identifier}/{start}/{end}
Allows: GET

Retrieves movies playing at a given cinema, specified by a non-case sensitive cinema name or id number, between given dates, in the format YYYY-MM-DD

####/cinema/suburb/{suburb}
Allows: GET

Retrieves a list of cinemas located in the supplied suburb (case insensitive)
