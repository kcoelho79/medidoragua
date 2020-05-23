class Watermeter:
    
    def __init__(self):
        self.url = 'https://datastudio.google.com/reporting/188wX_8wKVwiG8VBhAGheljpcqU18Dov1/page/bCkF'

    def fetch_data(self,url=None):
        if url:
            self.url = url

        print('(1)... fetching data from %s ...' %self.url)
        return self.url

    def convert_tocsv(self):
        print('(1)... converting dict to csv ...')
        pass

    def clean_data(self):
        pass


