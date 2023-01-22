# first import the module
import webbrowser

# then make a url variable
# getting path
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
# First registers the new browser
webbrowser.register('chrome', None,
                    webbrowser.BackgroundBrowser(chrome_path))
list =["https://portal.ostfalia.de/welcome","https://moodle.ostfalia.de/login/index.php","https://studip.ostfalia.de/index.php?again=yes","https://exchange.tu-clausthal.de/","https://studip.tu-clausthal.de/index.php?again=yes"]
for url in list:
    webbrowser.get('chrome').open(url)
    print(url)



# after registering we can open it by getting its code.

