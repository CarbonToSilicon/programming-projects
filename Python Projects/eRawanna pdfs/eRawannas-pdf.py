import time
import base64
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PyPDF2 import PdfMerger

print("Paste the eRawannas in the rawanna_no.csv file.")
print("Note: First clear the old data from the .csv file if you don't want to execute them.")
print("There should be one eRawanna number in each line in the .csv file.\n")

# Prompt user for their desired output format
print("Choose an output option:")
print("1: Download as separate PDFs")
print("2: Download separately and combine all into a single PDF")
user_choice = input("Enter 1 or 2: ").strip()

if user_choice not in ['1', '2']:
    print("Invalid choice. Defaulting to Option 1 (separate PDFs).")
    user_choice = '1'

# Read rawanna numbers from CSV
rawanna_numbers = []
if os.path.exists("rawanna_no.csv"):
    with open("rawanna_no.csv", "r") as data_file:
        for f in data_file:
            f = f.strip() 
            if f:
                rawanna_numbers.append(f)
else:
    print("Error: rawanna_no.csv not found in the current directory.")
    exit()

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    
    return webdriver.Chrome(options=chrome_options)

def print_rawannas():
    driver = setup_driver()
    
    print("\n--- Starting Batch PDF Generation with 94% Scaling ---")
    
    output_dir = "Rawanna_PDFs"
    os.makedirs(output_dir, exist_ok=True)
    
    # Keep track of successfully generated PDFs for merging later
    successful_pdfs = []
    
    try:
        for r_id in rawanna_numbers:
            url = f"https://mines.rajasthan.gov.in/DMG2/Public/eRawannaStatus/{r_id}"
            print(f"Loading {r_id}...")
            
            try:
                driver.get(url)
                time.sleep(5) # Wait for page to fully render
                
                print(f"Generating PDF for {r_id}...")
                
                # Use Chrome DevTools Protocol to generate the PDF 
                pdf_data = driver.execute_cdp_cmd("Page.printToPDF", {
                    "scale": 0.94,
                    "printBackground": True,
                    "displayHeaderFooter": False,
                    "marginTop": 0.078,
                    "marginBottom": 0.078,
                    "marginLeft": 0.078,
                    "marginRight": 0.078
                })
                
                file_path = os.path.join(output_dir, f"{r_id}.pdf")
                with open(file_path, "wb") as file:
                    file.write(base64.b64decode(pdf_data['data']))
                    
                print(f"Saved: {file_path}")
                successful_pdfs.append(file_path)
                
            except Exception as e:
                print(f"Error on {r_id}: {e}")
                
    finally:
        driver.quit()
        
        # If the user selected option 2, merge the successfully downloaded PDFs
        if user_choice == '2' and successful_pdfs:
            print("\n--- Merging PDFs ---")
            try:
                merger = PdfMerger()
                for pdf_path in successful_pdfs:
                    merger.append(pdf_path)
                
                merged_filename = "Combined_Rawannas.pdf"
                merger.write(merged_filename)
                merger.close()
                print(f"Success! All PDFs have been combined into: {merged_filename}")
            except Exception as e:
                print(f"Error while merging PDFs: {e}")

        print("\n--- Process Finished ---")

if __name__ == "__main__":
    print_rawannas()