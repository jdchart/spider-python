import os
import cv2
from PyPDF2 import PdfReader

class MediaFile:
    def __init__(self, path) -> None:
        """
        Represent a media file.
        
        Gather data about a media file and perform convertions.
        """

        self.path = path
        self.type = self.getType()
        self.data = self.getData()
        
    def getType(self):
        """Determine the media file's type."""

        accepted = [
            {"extension" : "mp4", "type" : "video"},
            {"extension" : "mpg", "type" : "video"},
            {"extension" : "png", "type" : "image"},
            {"extension" : "jpg", "type" : "image"},
            {"extension" : "jpeg", "type" : "image"},
            {"extension" : "pdf", "type" : "document"}
        ]

        ext = os.path.splitext(self.path)[1][1:]
        for item in accepted:
            if ext == item["extension"]:
                return [ext, item["type"]]
        return None
    
    def getData(self):
        """Parse metadata about the media file."""

        retData = {}

        if self.type[1] == "video":
            retData = self.parseVideo()
        if self.type[1] == "image":
            retData = self.parseImage()
        if self.type[1] == "document":
            retData = self.parseDocument()

        return retData
    
    def parseToSpiderNode(self):
        """Return a dict that can be used to create a spider node."""

        nodeData = {
            "title" : os.path.splitext(os.path.basename(self.path))[0],
            "format" : {
                "type" : self.type[1],
                "fileFormat" : self.type[0],
                "uri" : self.path
            },
            "instructionalMethod" : {
                "annotationDisplayScale" : 1,
                "annotationDisplayPos" : [0, 0],
                "annotationOverlay" : False,
                "annotationPaint" : True,
                "important" : False
            }
        }

        if "dimensions" in list(self.data.keys()):
            nodeData["format"]["fullDimensions"] = self.data["dimensions"]
            nodeData["format"]["region"] = [-1]

        if "duration" in list(self.data.keys()):
            nodeData["format"]["fullDuration"] = self.data["duration"]
            nodeData["format"]["start"] = -1
            nodeData["format"]["end"] = -1

        if "pages" in list(self.data.keys()):
            nodeData["format"]["pages"] = self.data["pages"]

        return nodeData

    def parseVideo(self):
        """Derrive information from a video file."""

        openCVvideo = cv2.VideoCapture(self.path)
        
        frames = openCVvideo.get(cv2.CAP_PROP_FRAME_COUNT)
        fps = openCVvideo.get(cv2.CAP_PROP_FPS)
        duration = int(round(frames / fps) * 1000)
        width = int(openCVvideo.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(openCVvideo.get(cv2.CAP_PROP_FRAME_HEIGHT))

        return {
            "frames" : int(frames),
            "fps" : int(fps),
            "duration" : duration,
            "dimensions" : [width, height]
        }

    def parseImage(self):
        """Derrive information from an image file."""
        
        openCVimg = cv2.imread(self.path, cv2.IMREAD_UNCHANGED)

        return {
            "dimensions" : [int(openCVimg.shape[1]), int(openCVimg.shape[0])]
        }

    def parseDocument(self):
        """Derrive information from a pdf file."""

        pdfFile = PdfReader(self.path)

        maxWid = pdfFile.pages[0].mediabox.width
        maxHeight = pdfFile.pages[0].mediabox.height

        for page in pdfFile.pages:
            if page.mediabox.width > maxWid:
                maxWid = page.mediabox.width
            if page.mediabox.height > maxHeight:
                maxHeight = page.mediabox.height

        return {
            "dimensions" : [int(maxWid), int(maxHeight)],
            "pages" : len(pdfFile.pages)
        }