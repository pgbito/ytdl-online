
import urllib,time
from http.server import BaseHTTPRequestHandler, HTTPServer

CHROME_EXECUTABLE_PATH = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
hostName = "localhost"
serverPort = 80


def encode(body: str):
    return bytes(f'{body}', "utf-8")


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
     if self.path.startswith('/download'):
              
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("powered-by", "pgbito")
        self.end_headers()

        from pytube import YouTube
        url=self.path.replace('/download?url=','')
        strr = YouTube(url).streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().url


        self.wfile.write(encode('<body style="background-color: black;color: white;text-align: center;"><h1>Redirecting to download...</h1></body><script>setTimeout(function(){window.location.assign("'+strr+'")},5000)</script>'))
     else:
         self.wfile.write(encode(str(open('./home.html').read())))
def start_browser():
  import subprocess
  
  subprocess.run(CHROME_EXECUTABLE_PATH + ' -new-tab ' +  f'http://{hostName}:{serverPort}')
if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))
    import threading
    t = threading.Thread(target=start_browser)
    t.start()

    try:
        r=threading.Thread(target=webServer.serve_forever) 
        r.start()
        r.join()
        
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")

