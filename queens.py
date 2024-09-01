import cv2
import numpy as np

def get_corners(image, n):
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    all_corners = cv2.goodFeaturesToTrack(gray, 100, 0.01, 10)
    all_corners = np.intp(all_corners)             
    all_corners = np.ndarray.tolist(all_corners)

    filtered_corners = []
    for i in range(len(all_corners)):
        filtered_corners.append([all_corners[i][0][0], all_corners[i][0][1]])
    filtered_corners = sorted(filtered_corners, key=lambda x: (x[1], x[0]), reverse=True)
    for i in range(len(filtered_corners)):
        if i % (n + 1) != 0:
            filtered_corners[i][1] = filtered_corners[i-1][1]

    filtered_corners = sorted(filtered_corners, key=lambda x: (x[1], x[0]), reverse=True)
    grid_corners = [filtered_corners[i] for i in range(len(filtered_corners) - (n+1)) if i % (n+1) != n]
    grid_corners = sorted(grid_corners, key=lambda x: (x[1], x[0]))
    return grid_corners

def create_grid_and_color_map(image, corners, n):

    grid = [[i for i in range(n)] for j in range(n)]
    color_count = {}
    
    k = 0
    for i in range(n):
        for j in range(n):
            coord = [corners[k][0] - 23, corners[k][1] - 23]
            grid[j][i] =  image[coord[0], coord[1]] # B G R FORMAT
            if tuple(image[coord[0], coord[1]]) not in color_count:
                color_count[tuple(image[coord[0], coord[1]])] = 0
            k += 1

    return (grid, color_count)

def valid(output_grid, grid, row, col, color_map, n):

    # Check row
    for i in range(len(output_grid[0])):
        if output_grid[row][i] == '👑' and col != i:
            return False
    
    # Check col
    for i in range(len(output_grid)):
        if output_grid[i][col] == '👑' and row != i:
            return False
    
    # Check neighbours 
    if row > 0 and col > 0 and output_grid[row - 1][col - 1] == '👑':
        return False
    if row > 0 and col < n - 1 and output_grid[row - 1][col + 1] == '👑':
        return False
    if row < n - 1 and col > 0 and output_grid[row + 1][col - 1] == '👑':
        return False
    if row < n - 1 and col < n - 1 and output_grid[row + 1][col + 1] == '👑':
        return False
    
    # Check colour
    if color_map[tuple(grid[row][col])] > 0:
        return False
    
    return True # valid position

def solve(output_grid, row, grid, color_map, n):
    
    if row >= n:
        return True
    else:

        for col in range(n):
            if valid(output_grid, grid, row, col, color_map, n):
                output_grid[row][col] = '👑'
                color_map[tuple(grid[row][col])] += 1
                if solve(output_grid, row + 1, grid, color_map, n):
                    return True
                
                output_grid[row][col] = '-'
                color_map[tuple(grid[row][col])] -= 1
        
    return False

def main():

    file_name = input("Enter file name: ")
    size = int(input("Enter size of grid (number of rows): "))
    image = cv2.imread(file_name)
    image = cv2.resize(image, (0,0), fx=0.75, fy=0.75)
    corners = get_corners(image, size)
    output_grid = [['-' for i in range(size)] for j in range(size)]
    grid, color_map = create_grid_and_color_map(image, corners, size)
    solve(output_grid, 0, grid, color_map, size)
    print("Solution:\n\n")
    for row in output_grid:
        print(*row)
    print("\n\n")
    
if __name__ == '__main__':
    main()