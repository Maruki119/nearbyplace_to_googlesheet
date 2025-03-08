**NEARBY SEARCH LOCATION AND SAVE TO GOOGLE SHEETS PROGRAM**

1.How to Use This Find nearby place program
-Login Google cloud with google email, Created profile and add payment medthod

2.Create Credentials and JSON Key
-Home > APIs & Services > Credentials > Create Credentials > Service account # then add information > done
-Go to profile that you created > KEY > ADD KEY > Create New Key > (choose JSON) > CREATE # then keep the file that you downloaded

3.Create API KEY
-HOME > APIs & Services > Credentials > Create Credentials > API KEY # then keep the API KEY

4.Enable API for use Google Maps, Google Drive, Google Sheets
-HOME > APIs & Services > search 'Places API' > Enable
-HOME > APIs & Services > search 'Google Sheets API' > Enable
-HOME > APIs & Services > search 'Google Drive API' > Enable

5.Install library for program
-python3 -m pip install requests pandas gspread google-auth

6.How to setup?
-Create Google Sheet and name it Like 'Cafe'
-Add permission in Google Sheet for Editor with Service Account(client_email) from 2 JSON file that you downloaded
-Replace all of this variable
    API_KEY = "YOUR API KEY" # from 3
    LOCATION = "location (lat,lng)"  # right click on google maps example "10.444444422121,10.111111122222"
    SERVICE_ACCOUNT_FILE = "C:/example/maximal-window-999999-9999999.json"  # Replace with your service account JSON

7.How to Use?
-Run the program
-Input Three data that requests
    1.Input Sheet Name that you Created # Cafe
    2.Input Type of data what do you want to search # cafe *Can see all type in dataType.txt file*
    3.Input Radius you want to search nearby # 1000 *meter or equal 1 km*

example
    Cafe
    cafe
    1000

8.Limit of this program
-You can only find 61 places in the same time
-Can't show photo or image
-It might has some error if you input radius too far
-You can search only type that appear in dataType

Make the program to EXE file (optional)
pyinstaller --onefile --hidden-import=gspread mapToSheets.py
pip install pyinstaller
pyinstaller --onefile --hidden-import=gspread --hidden-import=google.oauth2.service_account mapToSheets.py