import scrapy
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TimeoutError, TCPTimedOutError

class DemoSpider(scrapy.Spider):
    name = "demo"
    start_urls = [ 
      "http://www.httpbin.org/",              # HTTP 200 expected 
      "http://www.httpbin.org/status/404",    # Webpage not found  
      "http://www.httpbin.org/status/500",    # Internal server error 
      "http://www.httpbin.org:12345/",        # timeout expected 
      "http://www.httphttpbinbin.org/",       # DNS error expected 
   ]  
    
    def __init__(self):
        super(DemoSpider, self).__init__()
        self.status_list = []  # List to store response statuses
    
    def start_requests(self):
        for u in self.start_urls:
            yield scrapy.Request(
                u,
                callback=self.parse_httpbin,
                errback=self.errback_httpbin,
                dont_filter=True
            )

    def parse_httpbin(self, response):
        self.logger.info('Received response from {}'.format(response.url))
        # Add status and URL to their respective lists
        self.status_list.append((response.status,response.url))

    def errback_httpbin(self, failure):
        # Logs failures
        dt_val = ()
        self.logger.error(repr(failure))
        if failure.check(HttpError):
            response = failure.value.response
            self.logger.error("HttpError occurred on %s", response.url)
            dt_val = (response.status,response.url,"HttpError occurred")
        elif failure.check(DNSLookupError):
            request = failure.request
            self.logger.error("DNSLookupError occurred on %s", request.url)
            dt_val = (None,request.url,"DNSLookupError occurred")
        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error("TimeoutError occurred on %s", request.url)
            dt_val = (None,request.url,"TimeoutError occurred")

        self.status_list.append(dt_val)


    def closed(self, reason):
        # Print the stored status and URL values at the end
        print(self.status_list)
