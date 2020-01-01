from selenium import webdriver

# Check if title page is up and running
browser = webdriver.Firefox()
browser.get('http://127.0.0.1:8000/')
browser.refresh()
assert 'All courses' in browser.title