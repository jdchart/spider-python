# Collection of elements
import uuid
import utils
from PIL import Image, ImageDraw, ImageFont
import os

class Project:
    def __init__(self, parsingMatrixPath):
        self.parsingMatrix = utils.readJson(parsingMatrixPath)
        self.documents = []

    def addNewDocument(self, **kwargs):
        newDocument = Document(self.parsingMatrix, **kwargs)
        self.documents.append(newDocument)
        return newDocument
    
    def addDocuments(self, pathList):
        for item in pathList:
            loadedDocument = Document(self.parsingMatrix, load_path = item)
            self.documents.append(loadedDocument)

    def parseProject(self, **kwargs):
        fullDocs = {}
        docList = []
        for doc in self.documents:
            docMatrix = doc.parseDocument(
                draw = kwargs.get("draw", False),
                saveFile = os.path.join(kwargs.get("outputDir", os.getcwd()), doc.name + ".png")
            )
            fullDocs[doc.name] = docMatrix
            docList.append(docMatrix)
        utils.writeJson(fullDocs, os.path.join(kwargs.get("outputDir", os.getcwd()), "DATA.json"))
        drawCompass(docList, os.path.join(kwargs.get("outputDir", os.getcwd()), "COMPOSITE.png"))
        
class Document:
    def __init__(self, parsingMatrix, **kwargs):
        self.name = kwargs.get("name", "")
        self.uuid = kwargs.get('uuid', str(uuid.uuid4()))
        self.node_uuid = kwargs.get('node_uuid', str(uuid.uuid4()))
        self.parsingMatrix = parsingMatrix

        for item in parsingMatrix:
            setattr(self, item, None)

        if "load_path" in kwargs:
            self.read(kwargs.get("load_path"))

    def write(self, outPath):
        outData = {}
        for item in self.__dict__:
            if item != "parsingMatrix":
                outData[item] = getattr(self, item)

        utils.writeJson(outData, outPath)
    
    def read(self, readPath):
        readData = utils.readJson(readPath)
        for item in readData:
            setattr(self, item, readData[item])

    def parseDocument(self, **kwargs):
        fieldList = self.parseFields()    
        #print("Loss: " + str(getFieldListLoss(fieldList)))
        
        fullMatrix = getEmptyMatrix(self.parsingMatrix["skills"])

        fieldCount = 0
        for item in fieldList:
            if item["matrix"] != None:
                fieldCount = fieldCount + 1
                for typo in item["matrix"]:
                    fullMatrix[typo] = fullMatrix[typo] + item["matrix"][typo]

        for item in fullMatrix:
            fullMatrix[item] = fullMatrix[item] / fieldCount

        toDraw = []

        for item in fieldList:
            if item["matrix"] != None:
                toDraw.append({"matrix" : item["matrix"], "col" : [66, 167, 214], "drawShape" : False})
        
        toDraw.append({"matrix" : fullMatrix, "col" : [222, 113, 126], "drawShape" : True})

        if kwargs.get("draw", False):
            drawCompass(toDraw, kwargs.get("saveFile", os.path.join(os.getcwd(), self.name + '.png')))

        return {"matrix" : fullMatrix, "loss" : getFieldListLoss(fieldList), "col" : [222, 113, 126], "drawShape" : False}

    def parseFields(self):
        fieldList = []
        for feature in self.parsingMatrix:
            thisMatrix = getEmptyMatrix(self.parsingMatrix[feature])
            categoryList = self.parsingMatrix[feature].keys()
            foundFeature = False

            if getattr(self, feature) != None:
                foundFeature = True
                for item in getattr(self, feature):
                    for category in categoryList:
                        associatedTerms = self.parsingMatrix[feature][category]
                        for term in associatedTerms:
                            if item["typology"] == term:
                                thisMatrix[category] = thisMatrix[category] + 1
            
            if foundFeature == True:
                fieldList.append({
                    "feature" : feature,
                    "matrix" : normalizeMatrix(thisMatrix)
                })
            else:
                fieldList.append({
                    "feature" : feature,
                    "matrix" : None
                })

        return fieldList

def getEmptyMatrix(parsingMatrix):
    categoryList = parsingMatrix.keys()
    returnMatrix = {}
    for item in categoryList:
        returnMatrix[item] = 0
    return returnMatrix

def getFieldListLoss(fieldList):
    noneCount = 0
    for item in fieldList:
        if item["matrix"] == None:
            noneCount = noneCount + 1
    return ((noneCount * 100) / len(fieldList)) / 100

def normalizeMatrix(matrix):
    minVal = 0
    maxVal = 0
    for item in matrix:
        if matrix[item] < minVal:
            minVal = matrix[item]
        if matrix[item] > maxVal:
            maxVal = matrix[item]
    normalized = {}
    for item in matrix:
        normalized[item] = utils.rescale(matrix[item], minVal, maxVal, 0, 1)
    return normalized

def drawCompass(dataList, saveFile):

    imageDims = {
        "width" : 1000,
        "height" : 1000,
        "padding" : 10
    }
    imageStyle = {
        "lineWidth" : 4,
        "pointSize" : 8
    }

    finalImg = Image.new('RGBA',(imageDims["width"], imageDims["height"]), (250,250,250, 0))
    draw = ImageDraw.Draw(finalImg)

    

    for item in dataList:

        fillCol = (item["col"][0], item["col"][1], item["col"][2], 100)
        lineCol = (item["col"][0], item["col"][1], item["col"][2], 255)

        x1 = utils.rescale(item["matrix"]["adaptive"], 0, 1, imageDims["width"] * 0.5, imageDims["padding"])
        y1 = utils.rescale(item["matrix"]["adaptive"], 0, 1, imageDims["height"] * 0.5, imageDims["padding"])
        x2 = utils.rescale(item["matrix"]["plan_oriented"], 0, 1, imageDims["width"] * 0.5, imageDims["padding"])
        y2 = utils.rescale(item["matrix"]["plan_oriented"], 0, 1, imageDims["height"] * 0.5, imageDims["height"] - imageDims["padding"])
        x3 = utils.rescale(item["matrix"]["institutional"], 0, 1, imageDims["width"] * 0.5, imageDims["width"] - imageDims["padding"])
        y3 = utils.rescale(item["matrix"]["institutional"], 0, 1, imageDims["height"] * 0.5, imageDims["height"] - imageDims["padding"])
        x4 = imageDims["width"] * 0.5
        y4 = imageDims["height"] * 0.5

        if item["drawShape"]:
            draw.polygon(
                [
                    (
                        x1,
                        y1
                    ),
                    (
                        x2,
                        y2
                    ),
                    (
                        x3,
                        y3
                    ),
                    (
                        x4,
                        y4
                    )
                ],
                fill = fillCol,
                outline = lineCol,
                width = imageStyle["lineWidth"]
            )
    
        centroid = utils.getCentroid([[x1, y1], [x2, y2], [x3, y3], [x4, y4]])
        draw.ellipse(
            [centroid[0] - (imageStyle["pointSize"]*0.5), centroid[1]- (imageStyle["pointSize"]*0.5), centroid[0] + (imageStyle["pointSize"]*0.5), centroid[1] + (imageStyle["pointSize"]*0.5)],
            fill = lineCol
        )


    draw.line(
        (
            (imageDims["width"] * 0.5) - (imageStyle["lineWidth"] * 0.5), 
            imageDims["padding"], 
            (imageDims["width"] * 0.5) - (imageStyle["lineWidth"] * 0.5), 
            imageDims["height"] - imageDims["padding"]
        ),
        fill = (185, 187, 189),
        width = imageStyle["lineWidth"]
    )

    draw.line(
        (
            imageDims["padding"],
            (imageDims["height"] * 0.5) - (imageStyle["lineWidth"] * 0.5), 
            imageDims["width"] - imageDims["padding"], 
            (imageDims["height"] * 0.5) - (imageStyle["lineWidth"] * 0.5)
        ),
        fill = (185, 187, 189),
        width = imageStyle["lineWidth"]
    )

    fnt = ImageFont.truetype("Arial", 20)

    #LABELS

    informalSize = get_text_dimensions("Informal", fnt)
    textX = int((imageDims["width"] * 0.5) - (informalSize[0] * 0.5))
    textY = imageDims["padding"]
    draw.text((textX, textY), "Informal", font=fnt, fill=(0, 0, 0, 128))

    formalisationSize = get_text_dimensions("Formalisation", fnt)
    textX = int((imageDims["width"] * 0.5) - (formalisationSize[0] * 0.5))
    textY = imageDims["height"] - imageDims["padding"] - formalisationSize[1]
    draw.text((textX, textY), "Formalisation", font=fnt, fill=(0, 0, 0, 128))

    shortSize = get_text_dimensions("Short duration", fnt)
    textX = imageDims["padding"]
    textY = (imageDims["height"] * 0.5) - (shortSize[1] * 0.5)
    draw.text((textX, textY), "Short duration", font=fnt, fill=(0, 0, 0, 128))

    longSize = get_text_dimensions("Long duration", fnt)
    textX = imageDims["width"] - imageDims["padding"] - longSize[0]
    textY = (imageDims["height"] * 0.5) - (longSize[1] * 0.5)
    draw.text((textX, textY), "Long duration", font=fnt, fill=(0, 0, 0, 128))

    adaptiveSize = get_text_dimensions("Adaptive", fnt)
    textX = imageDims["width"] * 0.1
    textY = (imageDims["height"] * 0.1) - (adaptiveSize[1] * 0.5)
    draw.text((textX, textY), "Adaptive", font=fnt, fill=(0, 0, 0, 128))

    revisableSize = get_text_dimensions("Revisable", fnt)
    textX = (imageDims["width"] * 0.9) - revisableSize[0]
    textY = (imageDims["height"] * 0.1) - (revisableSize[1] * 0.5)
    draw.text((textX, textY), "Revisable", font=fnt, fill=(0, 0, 0, 128))

    planOrientedSize = get_text_dimensions("Plan oriented", fnt)
    textX = imageDims["width"] * 0.1
    textY = (imageDims["height"] * 0.9) - (planOrientedSize[1] * 0.5)
    draw.text((textX, textY), "Plan oriented", font=fnt, fill=(0, 0, 0, 128))

    institutionalSize = get_text_dimensions("Institutional", fnt)
    textX = (imageDims["width"] * 0.9) - institutionalSize[0]
    textY = (imageDims["height"] * 0.9) - (institutionalSize[1] * 0.5)
    draw.text((textX, textY), "Institutional", font=fnt, fill=(0, 0, 0, 128))

    finalImg.save(saveFile, "PNG")

def get_text_dimensions(text_string, font):
    # https://stackoverflow.com/a/46220683/9263761
    ascent, descent = font.getmetrics()

    text_width = font.getmask(text_string).getbbox()[2]
    text_height = font.getmask(text_string).getbbox()[3] + descent

    return (text_width, text_height)