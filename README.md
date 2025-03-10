# **NEARBY SEARCH LOCATION AND SAVE TO GOOGLE SHEETS PROGRAM**

## **1. How to Use This Find Nearby Place Program**
1. Login to Google Cloud with your Google email.
2. Create a profile and add a payment method.

## **2. Create Credentials and JSON Key**
1. Navigate to:  
   **Home > APIs & Services > Credentials > Create Credentials > Service account**
2. Add necessary information and complete the process.
3. Go to the profile you created:  
   **KEY > ADD KEY > Create New Key**  
   - Choose **JSON** format and **CREATE**.  
   - Download and keep the JSON file securely.

## **3. Create API KEY**
1. Navigate to:  
   **HOME > APIs & Services > Credentials > Create Credentials > API KEY**  
   - Save the generated API key.

## **4. Enable APIs for Google Maps, Google Drive, Google Sheets**
1. Navigate to:  
   **HOME > APIs & Services**  
   - Search **'Places API'** and **Enable**.  
   - Search **'Google Sheets API'** and **Enable**.  
   - Search **'Google Drive API'** and **Enable**.

## **5. Install Required Python Libraries**
Run the following command in the terminal:
```bash
python3 -m pip install requests pandas gspread google-auth
