import time
import base64
import os
import queue
import random
import shutil
import threading
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PyPDF2 import PdfMerger
from concurrent.futures import ThreadPoolExecutor

print("Paste the eRawannas in the rawanna_no.csv file.")
print("Note: First clear the old data from the .csv file if you don't want to execute them.")
print("There should be one eRawanna number in each line in the .csv file.\n")

print("Choose an output option:")
print("1: Download as separate PDFs")
print("2: Download separately and combine all into a single PDF")
user_choice = input("Enter 1 or 2: ").strip()

merged_filename = "Combined_Rawannas.pdf" # Default name

if user_choice == '2':
    custom_name = input("Enter a name for the final combined PDF (leave blank for default): ").strip()
    if custom_name:
        # Automatically add .pdf if the user forgot to type it
        if not custom_name.lower().endswith('.pdf'):
            custom_name += '.pdf'
        merged_filename = custom_name
elif user_choice not in ['1', '2']:
    print("Invalid choice. Defaulting to Option 1 (separate PDFs).")
    user_choice = '1'

script_start_time = time.time() 

rawanna_numbers = []
if os.path.exists("rawanna_no.csv"):
    with open("rawanna_no.csv", "r") as data_file:
        for f in data_file:
            r_id = f.strip() 
            if r_id:
                rawanna_numbers.append(r_id)
else:
    print("Error: rawanna_no.csv not found in the current directory.")
    exit()

MAX_WORKERS = 6
driver_pool = queue.Queue()

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-software-rasterizer") 
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    
    return webdriver.Chrome(options=chrome_options)

def fetch_single_pdf(r_id, output_dir):
    time.sleep(random.uniform(1.0, 4.0)) 
    
    driver = driver_pool.get() 
    max_retries = 3
    
    for attempt in range(max_retries):
        if attempt == 0:
            print(f"Loading {r_id}...")
        else:
            print(f"Retrying {r_id} (Attempt {attempt + 1} of {max_retries})...")
            
        try:
            url = f"https://mines.rajasthan.gov.in/DMG2/Public/eRawannaStatus/{r_id}"
            
            driver.set_page_load_timeout(60)
            driver.get(url)
            
            time.sleep(3.0) 
            
            pdf_data = driver.execute_cdp_cmd("Page.printToPDF", {
                "scale": 0.90, 
                "printBackground": True,
                "displayHeaderFooter": False,
                "marginTop": 0.078, "marginBottom": 0.078,
                "marginLeft": 0.078, "marginRight": 0.078
            })
            
            file_path = os.path.join(output_dir, f"{r_id}.pdf")
            with open(file_path, "wb") as file:
                file.write(base64.b64decode(pdf_data['data']))
                
            print(f"Saved: {file_path}")
            driver_pool.put(driver)
            return file_path
            
        except Exception as e:
            if attempt == max_retries - 1:
                print(f"Failed {r_id} after {max_retries} attempts. Last Error: {e}")
                driver_pool.put(driver)
                return None
                
            try:
                driver.quit()
            except:
                pass 
            
            print(f"Browser crashed on {r_id}. Rebooting browser...")
            driver = setup_driver()
            time.sleep(5)
            
# def print_rawannas():
#     num_rawannas = len(rawanna_numbers)
    
#     if num_rawannas == 0:
#         print("No eRawannas found in the file. Exiting.")
#         return

#     actual_workers = min(num_rawannas, MAX_WORKERS)
    
#     print(f"\n--- Initializing {actual_workers} background browsers... ---")
    
#     for i in range(actual_workers):
#         print(f"Starting browser {i+1} of {actual_workers}...")
#         driver_pool.put(setup_driver())
#         time.sleep(7) 
        
#     print("--- Starting Batch PDF Generation ---")
#     output_dir = "Rawanna_PDFs"
#     os.makedirs(output_dir, exist_ok=True)
#     successful_pdfs = []
    
#     try:
#         with ThreadPoolExecutor(max_workers=actual_workers) as executor:
#             results = executor.map(lambda r_id: fetch_single_pdf(r_id, output_dir), rawanna_numbers)

def boot_browsers_slowly(actual_workers):
    """This runs invisibly in the background, feeding browsers to the queue."""
    for i in range(actual_workers):
        driver_pool.put(setup_driver())
        print(f"Browser {i+1} joined the pool.")
        time.sleep(7) 

def print_rawannas():
    num_rawannas = len(rawanna_numbers)
    
    if num_rawannas == 0:
        print("No eRawannas found in the file. Exiting.")
        return

    actual_workers = min(num_rawannas, MAX_WORKERS)
    
    print(f"\n--- Initiating Rolling Start with {actual_workers} workers ---")
    
    # Start booting the browsers in the background (daemon=True means it closes safely when the script ends)
    threading.Thread(target=boot_browsers_slowly, args=(actual_workers,), daemon=True).start()
        
    print("--- Starting Batch PDF Generation Immediately ---")
    output_dir = "Rawanna_PDFs"
    os.makedirs(output_dir, exist_ok=True)
    successful_pdfs = []
    
    try:
        # We start the executor immediately. The workers will pull browsers as soon 
        # as the background thread creates them, OR reuse ones that finish quickly!
        with ThreadPoolExecutor(max_workers=actual_workers) as executor:
            results = executor.map(lambda r_id: fetch_single_pdf(r_id, output_dir), rawanna_numbers)
########
            for file_path in results:
                if file_path:
                    successful_pdfs.append(file_path)

        if user_choice == '2' and successful_pdfs:
            print("\n--- Merging PDFs ---")
            try:
                merger = PdfMerger()
                for pdf_path in successful_pdfs:
                    merger.append(pdf_path)
                
                merger.write(merged_filename)
                merger.close()
                print(f"Success! All PDFs have been combined into: {merged_filename}")
                
                # Deletes the temporary folder and all individual PDFs inside it
                print(f"Cleaning up temporary files...")
                shutil.rmtree(output_dir)
                print(f"Deleted the '{output_dir}' folder.")
                
            except Exception as e:
                print(f"Error while merging or cleaning up PDFs: {e}")
                
    finally:
        print("\nClosing background browsers...")
        while not driver_pool.empty():
            driver = driver_pool.get()
            driver.quit()
            
        total_time_seconds = time.time() - script_start_time
        minutes = int(total_time_seconds // 60)
        seconds = int(total_time_seconds % 60)
        
        print(f"\n--- Process Finished ---")
        print(f"Total Execution Time: {minutes} minutes and {seconds} seconds.")

if __name__ == "__main__":
    print_rawannas()