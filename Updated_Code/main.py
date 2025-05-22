import csv
import cv2
import numpy as np
import pandas as pd

def getAverageDistance(image):
    # Read the image in grayscale
    #image = cv2.imread('9861699_007_pred.png', cv2.IMREAD_GRAYSCALE)
    #image = cv2.imread('9002116_039_pred.png', cv2.IMREAD_GRAYSCALE)
    #image = cv2.imread('9002116_020_pred.png', cv2.IMREAD_GRAYSCALE)
    #image = cv2.imread('9002116_021_pred.png', cv2.IMREAD_GRAYSCALE)

    #image = cv2.imread('9002116_054_pred.png', cv2.IMREAD_GRAYSCALE)

    # # Create a color version of the image to draw colored boundaries 
    color_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    # Step 2: Ensure the image is in 8-bit format 
    image = cv2.convertScaleAbs(image)




    # Check the dimensions of the image
    #print(f'Image shape: {image.shape}')

    # Step 2: Convert the grayscale image to a binary image 
    _, binary_image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    #binary opening the image
    #kernel = np.ones((27,27), np.uint8)

    #opened_image = cv2.morphologyEx(binary_image, cv2.MORPH_OPEN, kernel)

    # # Save pixel values to CSV 
    # with open('image.csv', mode='w', newline='') as file: 
    #     writer = csv.writer(file) 
    #     writer.writerows(image) 

    # print("Pixel values have been saved to pixel_values.csv")

    # with open('binary_image.csv', mode='w', newline='') as file: 
    #     writer = csv.writer(file) 
    #     writer.writerows(binary_image) 

    #print("Pixel values have been saved to image.csv and binary_image.csv")

    # # Optionally, display the image using OpenCV
    # cv2.imshow('Grayscale Image', image)
    # cv2.imshow('Opened Image', opened_image)

    # Step 3: Find connected components with statistics 
    num_labels, labels_im, stats, centroids = cv2.connectedComponentsWithStats(binary_image)

    # Step 4: Extract areas of each label 
    areas = stats[:, cv2.CC_STAT_AREA] 

    # Print the areas of each label 
    # print(f'Number of connected components: {num_labels}') 

    # for label in range(num_labels): 
    #     print(f'Label {label} has an area of {areas[label]} pixels')


    # Sort indices based on the area 
    sorted_indices = np.argsort(areas)[::-1] 

    #print(sorted_indices)

    # Get pixel indices of the largest 2 connected components 
    largest_2_components = [] 

    max_y = 0

    selected_points_femur = []
    selected_points_tibia = []

    # Set the margin 
    margin = 30 # Adjust the margin as needed

    for i in range(1,3):
        component_mask = (labels_im == sorted_indices[i]).astype("uint8") 
        pixel_indices = np.column_stack(np.where(component_mask)) 
        largest_2_components.append(pixel_indices) 

        # Find contours 
        contours, _ = cv2.findContours(component_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        # Draw contours on the color image 

        if i == 1:
            cv2.drawContours(color_image, contours, -1, (0, 0, 255), 2) # RED color for label 1 boundaries
            # Get the largest y-coordinate for each contour 
            max_y = max([point[0][1] for contour in contours for point in contour])

            # Select points within the margin 
            for contour in contours: 
                for point in contour: 
                    if (point[0][1] >= max_y - margin) and (point[0][1] < max_y + margin): 
                        selected_points_femur.append(tuple(point[0]))

        else:
            cv2.drawContours(color_image, contours, -1, (255, 0, 0), 2) # Blue color for label 1 boundaries
            for contour in contours: 
                for point in contour: 
                    if (point[0][1] >= max_y - margin) and (point[0][1] < max_y + margin): 
                        selected_points_tibia.append(tuple(point[0]))

            if(selected_points_tibia == []):
                max_y = 192
                for contour in contours: 
                    for point in contour: 
                        if (point[0][1] >= max_y - margin) and (point[0][1] < max_y + margin): 
                            selected_points_tibia.append(tuple(point[0]))
            if selected_points_tibia == []:
                return [True]

            selected_points_tibia = sorted(selected_points_tibia, key=lambda point: point[0])

        

    # interpolated_points_femur = [] 
    # interpolated_points_tibia = [] 
    # for j in range(2):
    #     if j == 0:
    #         for i in range(len(selected_points_femur) - 1): 
    #             start_point = np.array(selected_points_femur[i]) 
    #             end_point = np.array(selected_points_femur[i + 1]) 
    #             # Linear interpolation 
    #             num_interp_points = int(np.linalg.norm(end_point - start_point)) 
    #             for j in range(num_interp_points): 
    #                 interp_point = start_point + (end_point - start_point) * (j / num_interp_points) 
    #                 interpolated_points_femur.append(tuple(interp_point.astype(int)))
    #     else:
    #         for i in range(len(selected_points_tibia) - 1): 
    #             start_point = np.array(selected_points_tibia[i]) 
    #             end_point = np.array(selected_points_tibia[i + 1]) 

    #             distance = np.linalg.norm(start_point - end_point)
    #             # if distance > 20:
    #             #     continue
    #             # Linear interpolation 
    #             num_interp_points = int(np.linalg.norm(end_point - start_point)) 
    #             for j in range(num_interp_points): 
    #                 interp_point = start_point + (end_point - start_point) * (j / num_interp_points) 
    #                 interpolated_points_tibia.append(tuple(interp_point.astype(int)))
        

        # Mark the pixels in the original image 
        # if i == 1:
        #     for (x, y) in pixel_indices: 
        #         color_image[x, y] = [0, 0, 255] # Mark with red color
        # else:
        #     for (x, y) in pixel_indices: 
        #         color_image[x, y] = [255, 0, 0] # Mark with red color
        
    # Display the pixel indices of the largest 2 components 
    # for idx, component in enumerate(largest_2_components, start=1): 
    #     print(f'Component {idx}:') 
    #     print(component)

    # Step 4: Normalize the label image to a range suitable for display 
    # labels_im_normalized = cv2.normalize(labels_im, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)

    # with open('labelled.csv', mode='w', newline='') as file: 
    #     writer = csv.writer(file) 
    #     writer.writerows(labels_im_normalized) 

    # Step 4: Display the original and labeled compenents images 
    # cv2.imshow('Original Image', binary_image) 
    # cv2.imshow('Connected Components', labels_im_normalized) 
    # cv2.waitKey(0) 
    # cv2.destroyAllWindows() 

    # # Save and display the labelled largest 2 colored result 
    # cv2.imwrite('marked_image.png', color_image) 
    # cv2.imshow('Marked Image', color_image) 
    # cv2.waitKey(0) 
    # cv2.destroyAllWindows()

    # Save and display the result 
    # cv2.imwrite('boundary_marked_image.png', color_image) 
    # cv2.imshow('Boundary Marked Image', color_image) 
    # cv2.waitKey(0) 
    # cv2.destroyAllWindows()

    # color_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    # for i in range(2):
    #     if i == 0:
    #         for (x, y) in selected_points_femur: 
    #                 color_image = cv2.circle(color_image, (x, y), 1, (0, 255, 0), -1) # Green color for selected points
    #     else:
    #         for (x, y) in selected_points_tibia: 
    #                 color_image = cv2.circle(color_image, (x, y), 1, (0, 255, 0), -1) # Green color for selected points

    # # Save and display the result 
    # cv2.imwrite('selected_points_image.png', color_image) 
    # cv2.imshow('Selected Points Image', color_image) 
    # cv2.waitKey(0) 
    # cv2.destroyAllWindows()

    # color_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    # for i in range(2):
    #     if i == 0:
    #         for (x, y) in interpolated_points_femur: 
    #                 color_image = cv2.circle(color_image, (x, y), 1, (0, 255, 0), -1) # Green color for selected points
    #     else:
    #         for (x, y) in interpolated_points_tibia: 
    #                 color_image = cv2.circle(color_image, (x, y), 1, (0, 255, 0), -1) # Green color for selected points

    # # Save and display the result 
    # cv2.imwrite('Interpolated_points_image.png', color_image) 
    # cv2.imshow('Interpolated Points Image', color_image) 
    # cv2.waitKey(0) 
    # cv2.destroyAllWindows()

    #functions for selecting points from tibia for minimum distance to femur

    def get_min_distance_pts(femur_points,tibia_points):

        minDistances = [[]for i in range(len(femur_points))]

        for i,f_point in enumerate(femur_points):
            minDist = 1e9
            for t_point in tibia_points:

                dist = np.linalg.norm(np.array(f_point) - np.array(t_point))

                if minDist > dist:
                    minDist = dist
                    minDistances[i] = t_point 

        return minDistances

    # color_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    # t_pts = get_min_distance_pts(selected_points_femur,selected_points_tibia)

    # # Ensure both arrays have the same number of points 
    # assert len(selected_points_femur) == len(t_pts), "The two arrays must have the same number of points" 
    # # Draw lines between corresponding points in yellow 
    # for point1, point2 in zip(selected_points_femur, t_pts): 
    #     cv2.line(color_image, point1, point2, (0, 255, 255), 1) # Yellow color with thickness 2 
        
    # # Save and display the result 
    # cv2.imwrite('lines_between_points_yellow.png', color_image) 
    # cv2.imshow('Lines Between Points', color_image) 
    # cv2.waitKey(0) 
    # cv2.destroyAllWindows()



    def get_distance(femur_points,tibia_points):

        minDistances = np.zeros(len(femur_points))

        for i,f_point in enumerate(femur_points):
            minDist = 1e9
            for t_point in tibia_points:
                minDist = min(minDist,np.linalg.norm(np.array(f_point) - np.array(t_point)))
            minDistances[i] = minDist
        
        part_length = len(minDistances) // 3

        final_array = np.zeros(3)

        part1 = minDistances[:part_length] 
        part2 = minDistances[part_length:2*part_length] 
        part3 = minDistances[2*part_length:]

        final_array[0] = min(part1)
        final_array[1] = min(part2)
        final_array[2] = min(part3)

        return final_array

    return get_distance(selected_points_femur,selected_points_tibia)

def Processable(img):
    # Step 2: Ensure the image is in 8-bit format 
    img = cv2.convertScaleAbs(img)

    # Step 2: Convert the grayscale image to a binary image 
    _, binary_image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Step 3: Find connected components with statistics 
    num_labels, labels_im, stats, centroids = cv2.connectedComponentsWithStats(binary_image)

    # Step 4: Extract areas of each label 
    areas = stats[:, cv2.CC_STAT_AREA] 

    # Print the areas of each label 
    # print(f'Number of connected components: {num_labels}') 

    # for label in range(num_labels): 
    #     print(f'Label {label} has an area of {areas[label]} pixels')


    count = 0

    for label in range(1,num_labels):
        if areas[label] > 5000:
            count+=1
        if count > 2:
            return False
    return True if count == 2 else False

# image = cv2.imread('9002116_054_pred.png', cv2.IMREAD_GRAYSCALE)

# image = cv2.imread('9861699_007_pred.png', cv2.IMREAD_GRAYSCALE)

# texts = ['9861699_007_pred.png','9002116_054_pred.png','9002116_039_pred.png','9002116_020_pred.png','9002116_021_pred.png', '9005075_077_pred.png','9002116_068_pred.png','9005075_050_pred.png', '9005075_072_pred.png', '9005132_122_pred.png']

# for i in range(len(texts)):
#     image = cv2.imread(texts[i], cv2.IMREAD_GRAYSCALE)
#     if Processable(image):
#         print(texts[i]+f': {getAverageDistance(image)}')
#     else:
#         print("No. of regions not valid")

# Read the CSV file
file_path = 'casenames.csv'  # Replace with the path to your CSV file
df = pd.read_csv(file_path)

falseValues = 65

cases = {}

#Display the dataframe
for i in range(len(df)):
    caseAverageDistances = []
    for j in range(1,161):
        image = cv2.imread(f'All_Images/{df.iloc[i,0]}_{j:03}_pred.png', cv2.IMREAD_GRAYSCALE)
        if Processable(image):
            imageAverageDistance = getAverageDistance(image)
            if imageAverageDistance[0] == True:
                continue
            if imageAverageDistance[0] > falseValues and imageAverageDistance[1] > falseValues and imageAverageDistance[2] > falseValues:
                continue
            caseAverageDistances.append(list(imageAverageDistance))
    
    print(f'For case {df.iloc[i,0]} samples checked: {len(caseAverageDistances)}')

    caseAverageDistances_DF = pd.DataFrame(caseAverageDistances)

    if i == 2:
        caseAverageDistances_DF.to_csv('dataframe.csv', index=False)

    caseAverageDistance = caseAverageDistances_DF.mean().tolist()

    cases[str(df.iloc[i,0])] = caseAverageDistance

# Specify the CSV file name 
csv_file = 'output.csv' 
# Write the dictionary to the CSV file 
with open(csv_file, mode='w', newline='') as file: 
    writer = csv.writer(file) 
    # Write the header 
    writer.writerow(['Case Name', 'Region 1', 'Region 2', 'Region 3']) 
    # Write the data 
    for key, values in cases.items(): 
        writer.writerow([key] + values)


    






        