import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# --- CONFIGURATION ---
#rawanna_input = input(f"Paste the eRawanna numbers here.\nThere should be 1 eRawanna number in each line and there should be no empty line or space or any other text.\n")
print(f"Paste the eRawannas in the rawanna_no.csv file.\nNote: First clear the old data from the .csv file if you don't want to execute them.\nThere should be one eRawanna number in each line in the .csv file.\n\n")

# rawanna_numbers =[]
# with open("rawanna_no.csv", "r") as data_file:
#     for f in data_file:
#         rawanna_numbers.append(f)
# rawanna_numbers = ["SNON1099976223", "SNON1099976858"]
rawanna_numbers =[]
with open("rawanna_no.csv", "r") as data_file:
    for f in data_file:
        f = f.rstrip()
        rawanna_numbers.append(f)
#print(rawanna_numbers)

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--kiosk-printing")
    # Added to ensure background graphics (like logos/lines) are printed
    chrome_options.add_argument("--print-to-pdf-no-header") 
    
    return webdriver.Chrome(options=chrome_options)

def print_rawannas():
    driver = setup_driver()
    
    print("--- Starting Batch Print with 94% Scaling ---")
    
    try:
        for r_id in rawanna_numbers:
            url = f"https://mines.rajasthan.gov.in/DMG2/Public/eRawannaStatus/{r_id}"
            print(f"Loading {r_id}...")
            
            try:
                driver.get(url)
                time.sleep(5) 
                
                # --- CSS INJECTION FOR SCALING ---
                # This script injects a 'style' tag that forces the page to 
                # scale to 95% and removes margins only during printing.
                scaling_script = """
                var style = document.createElement('style');
                style.innerHTML = `
                    @media print {
                        body {
                            zoom: 94%;
                        }
                        @page {
                            margin: 2mm;
                        }
                    }
                `;
                document.head.appendChild(style);
                """
                driver.execute_script(scaling_script)
                
                print(f"Triggering scaled print for {r_id}...")
                driver.execute_script("window.print();")
                
                time.sleep(5) 
                
            except Exception as e:
                print(f"Error on {r_id}: {e}")
                
    finally:
        print("\n--- Process Finished ---")
        driver.quit()

if __name__ == "__main__":
    print_rawannas()