from timeit import default_timer as timer

import cv2


class SelectedArea:
    def __init__(self, areaPoints, startTime=0.0):
        self.areaPoints = areaPoints
        self.activeTime = 0.1
        self.passiveTime = 0
        self.startTime = startTime
        self.count = 0
        self.id = 1


firstPoint = (0, 0)
secondPoint = (0, 0)
selectedAreasList = []

objectBoxCenterList = []


def SetFirstPoint(x, y):
    global firstPoint
    firstPoint = (x, y)


def SetSecondPoint(x, y):
    global secondPoint
    secondPoint = (x, y)


def AddArea():
    rectPoints = [(0, 0), (0, 0)]
    rectPoints[0] = firstPoint
    rectPoints[1] = secondPoint
    selectedAreasList.append(SelectedArea(rectPoints, timer()))


def DeleteArea(x, y):
    for selectedArea in selectedAreasList:
        if selectedArea.areaPoints[0][0] <= x <= selectedArea.areaPoints[1][0] and selectedArea.areaPoints[0][
            1] <= y <= selectedArea.areaPoints[1][1]:
            selectedAreasList.remove(selectedArea)


def ChangeAreaID(index, newId):
    selectedAreasList[index].id = newId


def update_area_time(selectedArea):
    areaIsActive = False
    for personBoxCenter in objectBoxCenterList:
        if selectedArea.areaPoints[0][0] <= personBoxCenter[0] <= selectedArea.areaPoints[1][0] and \
                selectedArea.areaPoints[0][1] <= personBoxCenter[1] <= selectedArea.areaPoints[1][1]:
            print('зона с id:' + str(selectedArea.id) + ' активна!')
            areaIsActive = True
            break

    if areaIsActive:
        selectedArea.activeTime = timer() - selectedArea.passiveTime - selectedArea.startTime
    else:
        selectedArea.passiveTime = timer() - selectedArea.activeTime - selectedArea.startTime


def draw_selectedArea_box(img, box_color=(0, 255, 255), show_label=True, update_time=True):
    for selectedArea in selectedAreasList:
        left = selectedArea.areaPoints[0][0]
        top = selectedArea.areaPoints[0][1]
        right = selectedArea.areaPoints[1][0]
        bottom = selectedArea.areaPoints[1][1]
        img = cv2.rectangle(img, (left, top), (right, bottom), box_color, 4)

        if show_label:
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_size = 0.7
            font_color = (180, 100, 200)
            # Output the labels that show the x and y coordinates of the bounding box center.
            text_x = 'id=' + str(selectedArea.id)
            cv2.putText(img, text_x, (left + 5, top + 20), font, font_size, font_color, 1, cv2.LINE_AA)

        if update_time:
            update_area_time(selectedArea)
    return img
