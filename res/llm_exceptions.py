class PdfFileInvalidFormat(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)

class InvalidCollectionName(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)