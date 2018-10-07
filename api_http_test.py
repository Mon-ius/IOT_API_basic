import base64
import sys
import requests as r

url_01 = "http://127.0.0.1:5000/res"
url_02 = "https://iotapi.monius.top/res"
url_03 = "https://xxiot.herokuapp.com/res"

urls = [url_01, url_02, url_03]

def get_test(res):
    q=r.get(res)
    print(q.json())

def post_test(res):
    q = r.post(res,json={"id":"233"})
    print(q.json())

def put_test(res):
    q = r.put(res)
    print(q.json())

def delete_test(res):
    q = r.delete(res)
    print(q.json())


if __name__ == '__main__':
    n = input("Input number for url : ")
    url = urls[int(n)];print(url)

    
    functionList = [get_test, post_test, put_test, delete_test]
    for foo in functionList:
        foo(url)
