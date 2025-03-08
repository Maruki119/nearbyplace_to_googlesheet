import requests
import gspread
from google.oauth2.service_account import Credentials

SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

#********************************************REPLACE VARIABLE HERE**********************************************
# Google Maps API Setup
API_KEY = "YOUR API KEY"
LOCATION = "location (lat,lng)"  # Replace with your location (lat,lng)

# Google Sheets API Setup
SERVICE_ACCOUNT_FILE = "C:/example/maximal-window-999999-9999999.json"  # Replace with your service account JSON
#***************************************************************************************************************

def fetch_data(type, RADIUS):
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": LOCATION,
        "radius": RADIUS,
        "type": type,  # You can change this to "cafe" or any other type you need
        "key": API_KEY
    }
    dataval = []

    while True:
        # Make the initial request to get places
        response = requests.get(url, params=params)
        data = response.json()

        if data.get("status") != "OK":
            print(f"Error fetching data: {data.get('error_message')}")
            return []

        # Process the current batch of results
        for result in data.get("results", []):
            place_id = result['place_id']
            
            # Fetch additional place details such as phone, website, and user ratings
            details_url = f"https://maps.googleapis.com/maps/api/place/details/json"
            details_params = {
                "place_id": place_id,
                "key": API_KEY
            }
            details_response = requests.get(details_url, params=details_params)
            details_data = details_response.json()

            # Extract additional details
            phone = details_data.get("result", {}).get("formatted_phone_number", "N/A")
            website = details_data.get("result", {}).get("website", "N/A")
            user_ratings_count = details_data.get("result", {}).get("user_ratings_total", 0)
            
            # Photo reference and URL
            photo_reference = result.get("photos", [{}])[0].get("photo_reference")
            photo_url = None
            if photo_reference:
                photo_url = fetch_photo_url(photo_reference)
            
            subdata = {
                "Name": result.get("name"),
                "Address": result.get("vicinity"),
                "Rating": result.get("rating"),
                "Photo URL": f'=IMAGE("{photo_url}")' if photo_url else '',  # Use IMAGE formula
                "Google Maps Link": f"https://www.google.com/maps/place/?q=place_id:{place_id}",
                "Phone": phone,
                "Website": website,
                "User Ratings Count": user_ratings_count
            }
            dataval.append(subdata)

        # Print the fetched data for debugging
        print("Fetched Data:")
        for subdata in dataval:
            print(subdata)
        
        # Check if there is a next page
        next_page_token = data.get("next_page_token")
        if next_page_token:
            params["pagetoken"] = next_page_token  # Use next_page_token for pagination
        else:
            break  # Exit the loop if no more pages are available

    return dataval

def fetch_photo_url(photo_reference):
    photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference={photo_reference}&key={API_KEY}"
    return photo_url

def save_to_google_sheets(data, SPREADSHEET_NAME):
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    client = gspread.authorize(creds)

    try:
        spreadsheet = client.open(SPREADSHEET_NAME)
    except gspread.exceptions.SpreadsheetNotFound:
        print(f"Spreadsheet '{SPREADSHEET_NAME}' not found. Creating a new one.")
        spreadsheet = client.create(SPREADSHEET_NAME)

    worksheet = spreadsheet.sheet1
    try:
        worksheet.clear()  # This should clear existing data if needed

        # Alternatively, manually delete rows if clearing doesn't work well
        # worksheet.delete_rows(1, worksheet.row_count)

        # Append header row only once
        worksheet.append_row(["Name", "Address", "Rating", "Photo", "Google Maps Link", "Phone", "Website", "User Ratings Count"])

        # Prepare the data in a list of lists format for batch append
        rows_to_append = [list(subdata.values()) for subdata in data]

        # Append all rows in a single request
        worksheet.append_rows(rows_to_append)
        print("Data successfully saved!")
    except Exception as e:
        print(f"Error writing to Google Sheet: {e}")

def main():
    while True:
        SPREADSHEET_NAME = input("Enter the Sheet name: ")
        type = input("Enter Type to search (e.g., cafe): ")
        RADIUS = int(input("Enter Radius to search (meters): "))
        
        data = fetch_data(type, RADIUS)
        if data:
            save_to_google_sheets(data, SPREADSHEET_NAME)
            print("Data saved to Google Sheets!")
        else:
            print("No data to save.")
        
        # Ask the user if they want to search again or exit
        exit_choice = input("Do you want to search again? ('y' or 'Y' to continue, any to exit): ").strip().lower()
        if exit_choice != 'y' and exit_choice != 'Y':
            print("Exiting program.")
            break

if __name__ == "__main__":
    main()
