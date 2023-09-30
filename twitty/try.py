from requests_html import HTMLSession

session = HTMLSession()
url = "https://twitter.com/PopBase/status/1706150864355037455"

r = session.get(url)
r.html.render(sleep=2)

tweet_text = r.html.find('.css-1dbjc4n.r-1s2bzr4', first=True)

print(tweet_text)