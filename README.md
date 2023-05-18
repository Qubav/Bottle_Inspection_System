# Bottle Inspection System
The project was created to allow the user to inspect the bottle by analyzing the photo. The program works only for specific bottles, filled with liquid of a specific color and placed on a specific background. The photos used in the project were taken by me.

Used libraries: OpenCV, NumPy, PyQt5

Program main stages:
- checking the bottle's brand
- checking if there is a label on the bottle and adding bounding boxes around label and cap(if there are there)
- checking if there is liquid inside bottle and adding line higlighing its level

Each main stage of program consists of smaller steps. Steps for each stage are listed bellow.

Checking for bottle's brand:
- getting image of bottles shape
- cropping image and scaling it to set bottle's witdh to fixed value
- comparison with example shapes

Checking if there is a label on the bottle and adding bounding boxes around label and cap(if there are there):
- finding key points on bottle photo and images with label example
- comparison found key points and determining if there is label that fits(or fits most)
- checking label and cap placement on photo
- adding bounding boxes to photo

Checking if there is liquid inside bottle and adding line higlighing its level:
- changing photo from BGR to HSV and adding masks
- checking if there is liquid by checking for number of pixels representing one of two possible colors of fluid and comparing this number to number of pixels that represents bottle shape
- checking liquid level by using lateral histogram and image with pixels representing liquid color colored white on black background
- adding red line highlighting liquid level to photo

# Demo:
GUI:\
![image](https://github.com/Qubav/Bottle_Inspection_System/assets/124883831/57697f7d-41ad-49e1-9a90-f460779e2539)

View with original bottle photo:\
![image](https://github.com/Qubav/Bottle_Inspection_System/assets/124883831/9d35fee3-a167-4d3d-b11f-027420042326)

Veiw with processed photo:\
![image](https://github.com/Qubav/Bottle_Inspection_System/assets/124883831/78b5ce1e-5d42-448b-bee6-0c87fb179c57)

Different bottle inspection examples:
![image](https://github.com/Qubav/Bottle_Inspection_System/assets/124883831/cdee85a8-7489-45c8-bded-36d202c84185)

![image](https://github.com/Qubav/Bottle_Inspection_System/assets/124883831/cb483ede-ed5b-41f3-8317-5022409166dd)

![image](https://github.com/Qubav/Bottle_Inspection_System/assets/124883831/03f8b754-52df-46ef-9e5b-f747ea005133)

![image](https://github.com/Qubav/Bottle_Inspection_System/assets/124883831/554f325e-a4c5-4d33-8df7-c38ee23014d2)

![image](https://github.com/Qubav/Bottle_Inspection_System/assets/124883831/5052caf9-1480-4ce3-93e3-c8652b0b3845)
