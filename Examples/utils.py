import os

def collectFiles(path):
    acceptedFormats = ["mp4", "png", "jpg", "pdf"]

    finalList = []
    for root, dirs, files in os.walk(path):
        for file in files:
            extension = os.path.splitext(file)[1][1:]
            if extension in acceptedFormats:
                finalList.append(os.path.join(root, file))
    return finalList