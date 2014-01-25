import tornado.ioloop
import tornado.web
import tornado.httpclient
import tornado.escape




BING_Request = "https://api.datamarket.azure.com/Bing/Search/Web?"\
        "Query=%%27%s%%27&$top=10&$format=json"

BING_Key = "Lk/BUx4rCRwLfX/Ti0ArjKvgwn3AS7+mXmUfCyjpNcM"




class MainHandler(tornado.web.RequestHandler):


    def get(self, path):
        print("path=%s" % path)
        self.render(path)




class DataHandler(tornado.web.RequestHandler):

    def get(self, path):
        print("DataHandler, path=%s" % path)
        isTask = True

        if (isTask):
            ret_data = {"value": "a_value"}
            self.write(ret_data)
        else:
            self.redirect("/search?query=" + path)




class SearchHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    def get(self, params):
        print("SearchHandler, params:%s" % params)
        query = self.get_argument("query")
        http = tornado.httpclient.AsyncHTTPClient()
        request = tornado.httpclient.HTTPRequest(
                BING_Request % tornado.escape.url_escape(query),
                auth_username=BING_Key,
                auth_password=BING_Key)
        http.fetch(request, callback=self.on_response)
        print("Request: " + BING_Request % query)


    def on_response(self, response):
        if response.error: raise tornado.web.HTTPError(500)
        json = tornado.escape.json_decode(response.body)
        self.write("Fetched " + str(len(json['d']['results'])) + 
                " results from Bing Web Search") 
        # self.render("index.html", items=items)
        self.finish()
        



application = tornado.web.Application([
    (r"/search?(.+)", SearchHandler),
    (r"/data/(.+)", DataHandler),
    (r"/(.+)", MainHandler),
])




if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
