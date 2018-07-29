import csv
import os.path

class CSVWriter:
    def __init__(self, filePath):
        self.filePath = filePath
        if (not self.checkPath(self.filePath)):
            with open(filePath, 'w', newline='') as csvfile:
                self.fieldnames = ['img', 'move', 'speed', 'topLeftDistance', 'topRightDistance', 'botLeftDistance', 'botRightDistance']
                self.writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
                self.writer.writeheader()

    def checkPath(self, filePath):
        print(os.path.isfile(filePath))
        return os.path.isfile(filePath)

    def writeToCSV(self, data):
        with open(self.filePath, 'a', newline='') as csvfile:
            print(data)
            self.fieldnames = ['img', 'move', 'speed', 'topLeftDistance', 'topRightDistance', 'botLeftDistance',
                               'botRightDistance']
            self.writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            self.writer.writerow(data)