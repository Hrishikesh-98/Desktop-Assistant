import time
from selenium import webdriver
from PyQt5.QtWidgets import QMessageBox
from selenium.webdriver.support.ui import WebDriverWait
import selenium as se
from process_language import Process
import webbrowser ,wikipedia , wolframalpha, pyautogui,os,requests
from bs4 import BeautifulSoup
import sqlite3
from nltk.corpus import stopwords

client = wolframalpha.Client('K274P4-9WHW5A2G5L')
connection = sqlite3.connect("mp4videos.db")

class CustomError(Exception):
    pass

class Fetcher:
    def __init__(self, url):
        options = se.webdriver.ChromeOptions()
        options.add_argument('headless')

        self.driver = se.webdriver.Chrome(r"C:\phantomjs-2.1.1-windows\bin\chromedriver",chrome_options=options)
        self.driver.wait = WebDriverWait(self.driver, 5)
        self.url = url

    def lookup(self):
        self.driver.get(self.url)
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        try:
            if soup.find("div", {"class": "Z0LcW"}):
                print("1")
                answer = soup.find("div", {"class": "Z0LcW"}).text
            elif soup.find("div", {"class": "webanswers-webanswers_table__webanswers-table"}):
                print("2")
                answer = soup.find("div", {"class": "webanswers-webanswers_table__webanswers-table"}).text
            elif soup.find("span", {"class": "ILfuVd"}).text:
                print("3")
                answer = soup.find("span", {"class": "ILfuVd"}).text
            elif soup.find("span", {"class": "wob_t"}):
                print("4")
                answer = soup.find("span", {"class": "wob_t"})
            elif soup.find("div", {"class": "vk_bk dDoNo gsrt"}).text:
                print("5")
                answer = soup.find("class", {"class": "vk_bk dDoNo gsrt"}.text)
            else:
                print("6")
                answer = "I don't know"
                print("out")

        except:
            print("7")
            answer = "I don't know"
        return answer

class find_answer:
    def answers(self,d,query,window, classifier, cv):
        print(query)
        start = query.split(" ")[0]
        print("start = " + start)
        if start == 'shutdown':
            reply = QMessageBox.question(window, "Close Window", "Are you sure to shutdown",
                                         QMessageBox.Yes | QMessageBox.No,
                                         QMessageBox.No)
            print(reply)
            if str(reply) == '16384':
                command = "shutdown /s"
                os.system(command)
                return 0
        process = Process()
        category = process.predict(query, classifier, cv)
        print(category)
        if category == 1:
            if category == 1:
                print("in else 2")
                keywords = ['open','work on','execute','run', 'visit']
                for keys in keywords:
                    if keys in query:
                        split = keys + " "
                        d.speak("opening...")
                        url = query.split(split)[1]
                        if "https://" or "wwww" in url:
                            webbrowser.open(url)
                            return 0
                        elif "." in query:
                            url = query.split('open ')[1]
                            if "https://" or "wwww" in url:
                                webbrowser.open(url)
                                return 0
                            else:
                                url = "https://wwww." + url + ".com"
                                webbrowser.open(url)
                                return 0
                        else:
                            query = query.split(keys)[1]
                            print("in else")
                            words = query.split()
                            print(words)
                            words = [word for word in words if not word in set(stopwords.words('english'))]
                            for word in words:
                                print('in for')
                                name = word
                                to_count = "SELECT count(path) from paths WHERE name='" + name + "';"
                                counting = connection.execute(to_count)
                                for count in counting:
                                    print(count[0])
                                    if count[0] == 0:
                                        pass
                                    elif count[0] == 1:
                                        to_get = "SELECT path from paths where name='" + name + "';"
                                        paths = connection.execute(to_get)
                                        for path in paths:
                                            d.speak("opening")
                                            to_execute = path[0]
                                            print(to_execute)
                                            os.popen(to_execute)
                                            return 0
                                    elif count[0] > 1:
                                        paths_are = "prishi"
                                        d.speak("there are multiple files with this name, there paths are")
                                        to_get = "SELECT path from paths where name='" + name + "';"
                                        paths = connection.execute(to_get)
                                        for path in paths:
                                            paths_are = paths_are + "\n" + path[0]
                                            print(paths_are)
                                        return paths_are
                                    elif count[0] < 1:
                                        d.speak("cannot find this file on system")
                                        return 0
                            if requests.get("https://www." + name + ".com").status_code == 200:
                                d.speak('opening')
                                webbrowser.open('https://www.' + name + '.com')
                                return 0

                            else:
                                query = query
                                d.speak('Searching...')
                                try:
                                    try:
                                        res = client.query(query)
                                        results = next(res.results).text
                                        if "insufficient" or "data not available" in results:
                                            raise CustomError
                                        d.speak('Got it.')
                                        return results

                                    except:
                                        f = Fetcher(r'https://www.google.com/search?q=' + query)
                                        answer = f.lookup()
                                        if answer is "I don't know":
                                            results = wikipedia.summary(query, sentences=2)
                                            d.speak('Got it.')
                                            return results
                                        else:
                                            return str(answer)

                                except:
                                    d.speak("Don't know, try searching it on google")
                                    webbrowser.open('www.google.com')

        elif category == 2:
            if 'play' in query:
                if ":" and "\\" and '.' in query:
                    path = query.split("play ")[1]
                    d.speak("playing..")
                    os.popen(path)
                    return 0
                else:
                    name = query.split('play ')[1]
                    words = int(name.count(" "))
                    print(words)
                    run = True
                    while run:
                        print(name)
                        name = "%" + name + "%"
                        '''to_count = "SELECT count(path) from paths WHERE name='" + name +\
                                   "' and ext in ('mp3','mp4','MP3','MP$','avi','AVI','mkv','MKV');"'''
                        to_count = "SELECT count(path) from paths WHERE name LIKE '" + name + "' and ext in" \
                                   "('mp3','mp4','MP3','MP$','avi','AVI','mkv','MKV');"
                        counting = connection.execute(to_count)
                        for count in counting:
                            print(count[0])
                            try:
                                if words == 0:
                                    d.speak("couldnot find such file")
                                    return 0
                                if count[0] == 1:
                                    '''to_get = "SELECT path from paths WHERE name='" + name +\
                                             "' and ext in ('mp3','mp4','MP3','MP$','avi','AVI','mkv','MKV');"'''
                                    to_get = "SELECT path from paths WHERE name LIKE '" + name + "' and ext in" \
                                             "('mp3','mp4','MP3','MP$','avi','AVI','mkv','MKV');"
                                    paths = connection.execute(to_get)
                                    for path in paths:
                                        d.speak("playing")
                                        to_execute = path[0]
                                        print(to_execute)
                                        os.popen(to_execute)
                                        return 0
                                elif count[0] > 1:
                                    paths_are = "prishi"
                                    d.speak("there are multiple files with this name, there paths are")
                                    '''to_get = "SELECT path from paths WHERE name='" + name +\
                                             "' and ext in ('mp3','mp4','MP3','MP$','.avi','AVI','mkv','MKV');"'''
                                    to_get = "SELECT path from paths WHERE name LIKE '" + name + "' and ext in" \
                                             "('mp3','mp4','MP3','MP$','avi','AVI','mkv','MKV');"
                                    paths = connection.execute(to_get)
                                    for path in paths:
                                        paths_are = paths_are + "\n" + path[0]
                                    return paths_are
                                else:
                                    name = name[::-1]
                                    name = name.split(" ",1)[1]
                                    name = name[::-1]
                                    print(name)
                                    words = words - 1
                            except:
                                d.speak("couldnot open the file")
                                return 0
            elif 'listen to' in query:
                name = query.split('listen to ')[1]
                words = int(name.count(" "))
                print(words)
                run = True
                while run:
                    print(name)
                    name = "%" + name + "%"
                    '''to_count = "SELECT count(path) from paths WHERE name='" + name +\
                                "' and ext in ('mp3','mp4','MP3','MP$','avi','AVI','mkv','MKV');"'''
                    to_count = "SELECT count(path) from paths WHERE name LIKE '" + name + "' and ext in" \
                                "('mp3','mp4','MP3','MP$','avi','AVI','mkv','MKV');"
                    counting = connection.execute(to_count)
                    for count in counting:
                        print(count[0])
                        try:
                            if words == 0:
                                d.speak("couldnot find such file")
                                return 0
                            if count[0] == 1:
                                '''to_get = "SELECT path from paths WHERE name='" + name +\
                                            "' and ext in ('mp3','mp4','MP3','MP$','avi','AVI','mkv','MKV');"'''
                                to_get = "SELECT path from paths WHERE name LIKE '" + name + "' and ext in" \
                                         "('mp3','mp4','MP3','MP$','avi','AVI','mkv','MKV');"
                                paths = connection.execute(to_get)
                                for path in paths:
                                    d.speak("playing")
                                    to_execute = path[0]
                                    print(to_execute)
                                    os.popen(to_execute)
                                    return 0
                            elif count[0] > 1:
                                paths_are = "prishi"
                                d.speak("there are multiple files with this name, there paths are")
                                '''to_get = "SELECT path from paths WHERE name='" + name +\
                                            "' and ext in ('mp3','mp4','MP3','MP$','.avi','AVI','mkv','MKV');"'''
                                to_get = "SELECT path from paths WHERE name LIKE '" + name + "' and ext in" \
                                         "('mp3','mp4','MP3','MP$','avi','AVI','mkv','MKV');"
                                paths = connection.execute(to_get)
                                for path in paths:
                                    paths_are = paths_are + "\n" + path[0]
                                return paths_are
                            else:
                                name = name[::-1]
                                name = name.split(" ",1)[1]
                                name = name[::-1]
                                print(name)
                                words = words - 1
                        except:
                            d.speak("couldnot open the file")
                            return 0
            elif 'watch' in query:
                name = query.split('watch ')[1]
                words = int(name.count(" "))
                print(words)
                run = True
                while run:
                    print(name)
                    name = "%" + name + "%"
                    '''to_count = "SELECT count(path) from paths WHERE name='" + name +\
                                "' and ext in ('mp3','mp4','MP3','MP$','avi','AVI','mkv','MKV');"'''
                    to_count = "SELECT count(path) from paths WHERE name LIKE '" + name + "' and ext in" \
                                "('mp3','mp4','MP3','MP$','avi','AVI','mkv','MKV');"
                    counting = connection.execute(to_count)
                    for count in counting:
                        print(count[0])
                        try:
                            if words == 0:
                                d.speak("couldnot find such file")
                                return 0
                            if count[0] == 1:
                                '''to_get = "SELECT path from paths WHERE name='" + name +\
                                            "' and ext in ('mp3','mp4','MP3','MP$','avi','AVI','mkv','MKV');"'''
                                to_get = "SELECT path from paths WHERE name LIKE '" + name + "' and ext in" \
                                         "('mp3','mp4','MP3','MP$','avi','AVI','mkv','MKV');"
                                paths = connection.execute(to_get)
                                for path in paths:
                                    d.speak("playing")
                                    to_execute = path[0]
                                    print(to_execute)
                                    os.popen(to_execute)
                                    return 0
                            elif count[0] > 1:
                                paths_are = "prishi"
                                d.speak("there are multiple files with this name, there paths are")
                                '''to_get = "SELECT path from paths WHERE name='" + name +\
                                            "' and ext in ('mp3','mp4','MP3','MP$','.avi','AVI','mkv','MKV');"'''
                                to_get = "SELECT path from paths WHERE name LIKE '" + name + "' and ext in" \
                                         "('mp3','mp4','MP3','MP$','avi','AVI','mkv','MKV');"
                                paths = connection.execute(to_get)
                                for path in paths:
                                    paths_are = paths_are + "\n" + path[0]
                                return paths_are
                            else:
                                name = name[::-1]
                                name = name.split(" ",1)[1]
                                name = name[::-1]
                                print(name)
                                words = words - 1
                        except:
                            d.speak("couldnot open the file")
                            return 0

        elif category == 3:
            print("in")
            terms = ['pc','computer','system','locally','file explorer']
            keywords = ['find','locate','search','where']
            for term in terms:
                if term in query:
                    print(term)
                    words = query.split()
                    loc = words.index(term)
                    length = len(words) - 1
                    print(loc)
                    print(length)
                    print(words[loc-1])
                    if loc == length:
                        if words[loc-1] == 'on':
                            print("on")
                            d.speak('searching')
                            for keys in keywords:
                                if keys in query:
                                    split1 = keys + " "
                                    split2 = " on " + term
                                    query = query.split(split1)[1]
                                    query = query.split(split2)[0]
                                    query = "%" + query + "%"
                                    to_count = "SELECT count(path) from paths WHERE name LIKE '" + query + "';"
                                    counting = connection.execute(to_count)
                                    for count in counting:
                                        if count[0] > 0:
                                            to_get = "SELECT path from paths WHERE name LIKE '" + query + "';"
                                            paths = connection.execute(to_get)
                                            answer = "prishi"
                                            for path in paths:
                                                answer = answer + "\n" + path[0]
                                            return answer
                                        else:
                                            print("else fourth last")
                                            d.speak("could not find file on system, try searching on explorer")
                                            os.popen("C:\\Windows\\explorer.exe")
                                            return 0

                        else:
                            if loc == length:
                                d.speak('searching')
                                for keys in keywords:
                                    if keys in query:
                                        split1 = keys + " "
                                        split2 = " " + term
                                        query = query.split(split1)[1]
                                        query = query.split(split2)[0]
                                        query = "%" + query + "%"
                                        to_count = "SELECT count(path) from paths WHERE name LIKE '" + query + "';"
                                        counting = connection.execute(to_count)
                                        for count in counting:
                                            if count[0] > 0:
                                                to_get = "SELECT path from paths WHERE name LIKE '" + query + "';"
                                                paths = connection.execute(to_get)
                                                answer = "prishi"
                                                for path in paths:
                                                    answer = answer + "\n" + path[0]
                                                return answer
                                            else:
                                                print("else third last")
                                                d.speak("could not find file on system, try searching on explorer")
                                                os.popen("C:\\Windows\\explorer.exe")
                                                return 0

                            else:
                                d.speak('searching')
                                for keys in keywords:
                                    if keys in query:
                                        split1 = keys + " "
                                        query = query.split(split1)[1]

                                query = query.split(split2)[0]
                                query = "%" + query + "%"
                                to_count = "SELECT count(path) from paths WHERE name LIKE '" + query + "';"
                                counting = connection.execute(to_count)
                                for count in counting:
                                    if count[0] > 0:
                                        to_get = "SELECT path from paths WHERE name LIKE '" + query + "';"
                                        paths = connection.execute(to_get)
                                        answer = "prishi"
                                        for path in paths:
                                            answer = answer + "\n" + path[0]
                                        return answer
                                    else:
                                        print("else second last")
                                        d.speak("could not find file on system, try searching on explorer")
                                        os.popen("C:\\Windows\\explorer.exe")
                                        return 0

            for keys in keywords:
                if keys in query:
                    split = keys + " "
                    query = query.split(split)[1]
                    query = "%" + query + "%"
                    to_count = "SELECT count(path) from paths WHERE name LIKE '" + query + "';"
                    counting = connection.execute(to_count)
                    for count in counting:
                        if count[0] > 0:
                            to_get = "SELECT path from paths WHERE name LIKE '" + query + "';"
                            paths = connection.execute(to_get)
                            answer = "prishi"
                            for path in paths:
                                answer = answer + "\n" + path[0]
                            return answer
                        else:
                            print("else last")
                            d.speak("could not find file on system, try searching on explorer")
                            os.popen("C:\\Windows\\explorer.exe")
                            return 0

        elif category == 4:
            keywords = ['search','surf','look up','look']
            sites = ['youtube','google']
            print(sites)
            for site in sites:
                print(site)
                if site in query:
                    print(site)
                    if site is 'youtube':
                        site_url = "https://www.youtube.com/results?search_query="
                    else:
                        site_url = "https://www.google.com/search?q="
                    words = list()
                    words = query.split()
                    loc = words.index(site)
                    length = len(query.split())
                    if loc+1 == length:
                        if words[loc-1] == "on":
                            d.speak('okay')
                            split = "on " + site
                            query = query.split(split)[0]
                            for keys in keywords:
                                if keys in query:
                                    query = query.split(keys)[1]
                                    count = query.count(" ")
                                    query = query.replace(" ", '+', count)
                                    print(query)
                                    webbrowser.open(site_url + query)
                                    return 0
                        else:
                            d.speak('okay')
                            query = query.split(site)[0]
                            for keys in keywords:
                                if keys in query:
                                    query = query.split(keys)[1]
                                    count = query.count(" ")
                                    query = query.replace(" ", '+', count)
                                    webbrowser.open(site_url + query)
                                    return 0
                    elif loc+1 < length:
                        print(str(length) + "," + str(loc+1))
                        if words[loc+1] is "and":
                            for keys in keywords:
                                if words[loc+2] == keys:
                                    d.speak('okay')
                                    split = site + ' and ' + keys
                                    query = query.split(split)[1]
                                    count = query.count(" ")
                                    query = query.replace(" ", '+', count)
                                    webbrowser.open(site_url + query)
                                    return 0
                        else:
                            for keys in keywords:
                                if words[loc+1] == keys:
                                    d.speak('okay')
                                    split = site + ' ' + keys
                                    query = query.split(split)[1]
                                    count = query.count(" ")
                                    query = query.replace(" ", '+', count)
                                    webbrowser.open(site_url + query)
                                    return 0
                            d.speak('okay')
                            query = query.split(site)[1]
                            for keys in keywords:
                                if keys in query:
                                    query = query.split(keys)[1]
                                    count = query.count(" ")
                                    query = query.replace(" ", '+', count)
                                    webbrowser.open(site_url + query)
                                    return 0
                            webbrowser.open(site_url + query)
                            return 0

            d.speak('okay')
            end_pattern = ['over internet','over net','on the internet', 'on internet','on net','globally']
            for end in end_pattern:
                if end in query:
                    query = query.split(end)[0]
            for keys in keywords:
                if keys in query:
                    query = query.split(keys)[1]
                    webbrowser.open("https://www.google.com/search?q=" + query)
                    return 0
            webbrowser.open("https://www.google.com/search?q=" + query)
            return 0

        elif category == 5:
            if "type this " in query:
                message = query.split("type this ")[1]
            else:
                message = query.split("type ")[1]
            os.popen("C://Windows\\notepad.exe")
            time.sleep(3)
            pyautogui.typewrite(message)
            return 0
        elif category == 6:
            if "how" in query:
                print("in how")
                words = query.split()
                new_text = "wikihow "+ query
                print(new_text)
                params = {"q": new_text}
                r = requests.get("https://www.bing.com/search", params=params)
                soup = BeautifulSoup(r.text, "html.parser")
                results = soup.find("ol", {"class": "b_results"})
                links = soup.findAll("li", {"class": "b_algo"})
                run = True
                for item in links:
                    if run:
                        item_href = item.find('a').attrs['href']
                        if "www.wikihow" in item_href:
                            item_href = str(item_href)
                            item_href = item_href.split("=", 1)[-1]
                            item_href = item_href.split("&", 1)[0]
                            f = requests.get(item_href)
                            soup = BeautifulSoup(f.text, "html.parser")
                            steps = soup.findAll("b", {"class": "whb"})
                            print("steps" , steps)
                            answer = ""
                            if steps:
                                print(len(steps))
                                count = 1
                                for step in steps:
                                    if count < len(steps):
                                        answer = answer + "\n" + str(count) + " " + step.text + "\n "
                                        count +=1
                                        globals()['run'] = False
                                    else:
                                        break
                                return answer
                        else:
                            query = query
                            d.speak('Searching...')
                            try:
                                try:
                                    res = client.query(query)
                                    results = next(res.results).text
                                    if "insufficient" or "data not available" in results:
                                        raise CustomError
                                    d.speak('Got it.')
                                    return results

                                except:
                                    f = Fetcher(r'https://www.google.com/search?q=' + query)
                                    answer = f.lookup()
                                    if answer is "I don't know":
                                        results = wikipedia.summary(query, sentences=2)
                                        d.speak('Got it.')
                                        return results
                                    else:
                                        return str(answer)

                            except:
                                d.speak("Don't know, try searching it on google")
                                webbrowser.open('www.google.com')

            else:
                query = query
                d.speak('Searching...')
                try:
                    try:
                        res = client.query(query)
                        results = next(res.results).text
                        if "insufficient" or "data not available" in results:
                            raise CustomError
                        d.speak('Got it.')
                        return results

                    except:
                        f = Fetcher(r'https://www.google.com/search?q=' + query)
                        answer = f.lookup()
                        if answer is "I don't know":
                            results = wikipedia.summary(query, sentences=2)
                            d.speak('Got it.')
                            return results
                        else:
                            return str(answer)

                except:
                    d.speak("Don't know, try searching it on google")
                    webbrowser.open('www.google.com')