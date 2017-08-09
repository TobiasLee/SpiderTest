import requests
import json
import time

with open('reporterAreas.json', 'r') as f:
    data = json.load(f)


ret = data['results']
# 2012 : 10 11 12
# 2014 2015
country_list = []
for item in ret:
    country_list.append(item['id'])


base3 = "&p=156&rg=all&cc=AG6&fmt=csv"
base1 = "https://comtrade.un.org/api/get?max=50000&type=C&freq=M&px=HS&ps="
base2 = "&r="

y1 = "2014"
y2 = "2015"
periods = [y1 + str("%02d" %  i) for i in range(1, 13)]
for obj in list(y2 + str("%02d" % i) for i in range(1, 13)):
    periods.append(obj)

periods.append("201210")
periods.append("201211")
periods.append("201212")
print(periods)

htmls = []
ids = []
#

for ps in periods:
    html1 = base1 + ps
    # print(html1)
    for id in country_list:
        html = html1 + base2 + id + base3
        htmls.append(html)
    # print(htmls[-1])


urls = htmls[1:]

i = 0
total = len(urls)
proxy_test ={"http": "http://122.72.32.73:80",
             "https": "https://182.34.22.136:808"}
for url in urls:
    print("downloading:" + url)
    month_idx = url.index("ps=")
    country_idx = url.find("r=")

    country = "".join(list(filter(str.isdigit,url[country_idx+2: country_idx+5])))
    YYMM = url[month_idx + 3: month_idx + 9]
    fileName = "country_" + country + "_time_" + YYMM
    r = requests.get(url, proxies=proxy_test)
    code = r.status_code
    if code == 409:
        print("Frequency is beyond limit!!")
        time.sleep(300)
    try:
        with open("./trade/" + fileName + ".csv", "wb") as f:
            f.write(r.content)
        i += 1
        print("Finished %d" % i,"of %d" % total)
        time.sleep(3)
    except:
        pass

print("Finished")


