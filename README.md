# Osteoarthritis Detection
Osteoarthritis (OA) is the most common form of arthritis in the knee. Cartilage is the slippery tissue on the ends of bones, in between joints, and elsewhere in the body. The thickness of cartilage is an important biomarker to access the severity of knee OA. In this project, we will process a sequence of bone mask images, which are segmented from knee MRI images using an automatic segmentation method called U-net, a convolutional neural network (CNN) that was developed for image segmentation.

# Objective:
The objective of this study is to develop an algorithm to measure the distance between femur and tibia bones in the bone masks. We shall use the distances measured accross various points between the Femur and Tibia as features to predict the severity level of knee OA.

# Steps to run the code:
-> Use all code from 'Updated_Code' directory with the All_images directory within it.

-> Remove the example image file and download all segmented images in the 'All_Images' directory inside the 'Updated_code' directory. You can find all the images on this link: https://drive.google.com/file/d/1pp0FhhMwLZ5mO1wlgtEt8c2W42kl3TXS/view?usp=sharing   

-> run 'pip install -r requirement.txt' to install all python libraries.

-> Run main.py using you Python interpretor [runtime environment Python 3.12.6]. (Code takes about 25-30 mins to process all the images).   

-> Bring the data into the format as shown in file CV_Data.csv file in the 'content' directory within the 'Updated_Code' directory (keep label column as the same in CV_Data.csv).  

-> Alternatively, you can also use the CV_Data.csv file to train and test the model.  

-> Run this data over the blocks of code as put in the 'ML_models_code.ipynb' (you can use Google Colab).


