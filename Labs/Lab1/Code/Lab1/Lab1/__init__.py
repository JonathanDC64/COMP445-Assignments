import get
import post

host = 'httpbin.org'
print(get.get(host, '/get?a=6&h=8&c=4').get_body())
print('\n\n\n')
print(post.post(host, '/post', {'a': '6', 'h': '8', 'c': '4'}).get_body())
