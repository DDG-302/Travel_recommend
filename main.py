from Crawlers import Attraction_crawler, Experience_crawler

exc = Experience_crawler(limit=40)
exc.run()

atc = Attraction_crawler()
atc.run()