from fastapi import HTTPException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def scrap_website(url):
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        # Iniciar o chrome
        driver = webdriver.Chrome(options = options)
        driver.get(url)
        page_content = driver.page_source
        driver.quit()
        
        return page_content
    
    except Exception as e:
        raise HTTPException(status_code=500, detail = str(e))
        