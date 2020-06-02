def MMultiply (L,R):
    NewMatrix = []
    if len(L[0]) != len(R):
        raise ValueError("Dimensional Error")
    else:
        for n in range(len(L[0])):
            NewMatrix.append([])
        for Row in range(len(L[0])):
            for Column in range(len(R[0])): ## NOT SURE ABOUT THE NAME COLUMN 
                num = 0
                for RN in range(len(L[Row])):
                    num += L[Row][RN]*R[RN][Column]
                NewMatrix[Row].append(num)
        return(NewMatrix)
def coordinatestomatrix(coords):
    matrix = [[],
              []]
    for coord in coords:
        matrix[0].append(coord[0])
        matrix[1].append(coord[1])
    return(matrix)
def matrixtocoordinates(matrix):
    coords = []
    for n in range(len(matrix[0])):
        coords.append([])
    for n in range(len(matrix[0])):
        coords[n].append(matrix[0][n])
        coords[n].append(matrix[1][n])
    return(coords)
