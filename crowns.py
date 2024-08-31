import cv2
import numpy as np

img = cv2.imread('test_file.png')
img = cv2.resize(img, (0,0), fx=0.75, fy=0.75)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

corners = cv2.goodFeaturesToTrack(gray, 100, 0.01, 10)
corners = np.int0(corners)
                  
#print(corners)
corners = np.ndarray.tolist(corners)

proper_corners = []
n = 6

for i in range(len(corners)):
    proper_corners.append([corners[i][0][0], corners[i][0][1]])

proper_corners = sorted(proper_corners, key=lambda x: (x[1], x[0]), reverse=True)

for i in range(len(proper_corners)):
    if i % 6 != 0:
        proper_corners[i][1] = proper_corners[i-1][1]

sorted_list = sorted(proper_corners, key=lambda x: (x[1], x[0]), reverse=True)

new_corners = [sorted_list[i] for i in range(len(sorted_list) - 6) if i % 6 != 5]

new_corners = sorted(new_corners, key=lambda x: (x[1], x[0]))

print(new_corners)
print(len(new_corners))


#cv2.imshow('Frame', img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()


# CREATE GRID NOW 

grid = [[i for i in range(5)] for j in range(5)]
hashmap = {}
k = 0
for i in range(5):
    for j in range(5):
        coord = [new_corners[k][0] - 30, new_corners[k][1] - 30]
        grid[j][i] =  img[coord[0], coord[1]] # B G R FORMAT
        #print(coord)
        #print(img[coord[0], coord[1]])
        if tuple(img[coord[0], coord[1]]) not in hashmap:
            hashmap[tuple(img[coord[0], coord[1]])] = 0
        k += 1

print(grid)

# SOLVE 

solve_grid = [['-' for i in range(5)] for j in range(5)]

print(solve_grid)