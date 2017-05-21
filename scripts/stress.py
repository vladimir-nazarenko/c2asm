import http.client
import urllib.parse

http.client.HTTPConnection.debuglevel = 1


code = """
#include <iostream>

int main()
{
    std::cout << "Hello world!" << std::endl;
    return 0;
}
"""

params = urllib.parse.urlencode(
    {'code': code, 'compiler': 'GCC 6.3', 'optimization_level': '-O3'}
)


headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 
    'X-Requested-With': 'XMLHttpRequest'
}

conn = http.client.HTTPConnection("c2asm.com")
try:
    conn.request('GET', '/assembly/' + '?' + params, None, headers)
    response = conn.getresponse()
    print(response.status, response.reason)

    data = response.read()
    print(data)
finally:
    conn.close()
