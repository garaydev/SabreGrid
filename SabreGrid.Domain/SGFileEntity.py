class SGFileEntity(object):
    """Common class for SGFiles"""

    FileName = ''
    FileSize = ''
    FileCreatedDate = ''

    def __init__(self,fName,fSize,fCreateDate):
        self.FileName = fName
        self.FileSize = fSize
        self.FileCreatedDate = fCreateDate

    def GetFileExtension(self):
        if self.FileName is not None:
           exten = os.path.splitext(self.FileName)[1]
           if exten is not None:
               return exten
        else:
            return None


