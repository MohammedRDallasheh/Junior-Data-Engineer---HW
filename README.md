# Junior-Data-Engineer---HW

In order to enable the service, run solution.py as a python file, in a folder that contains the csv files.

Working with the service:
    The service will ask you to enter a command. enter one of the following commands:
        - keepalive : to check if the service is alive.
        - userStats : the service will ask you then to enter user_id. enter a user_id to get the Stats.
        - sessionId : the service will ask you then to enter session_id. enter a session_id to get the requested information.
        - Kill : (don't forget to capitalize the "K") the service will shut down.


Improvements:
    - I suggest that you analyze which type of ads each user clicks, so next time when the user opens an app with placement for an ad, you inform sites (type
    of sites) that interest this user, that this user is more likely to click the ad, so they can bid higher.
    for example, the user clicks ebay and aliexpress, so he is interested in online shopping, so next time, you should inform sites like ebay, aliexpress,
    amazon etc, that this user is more likely to press the ad, so they can bid higher and increase thier chances to get an impression.
    - Following the previous suggested improvement, the /userStats route should be modified: the interests of the user should be included in the output.
