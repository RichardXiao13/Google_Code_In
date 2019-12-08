import geopandas
import matplotlib.pyplot as plt
import os

# Get directory with roads
path = os.getcwd() + "\\roads"
print(path)

# Go through each folder in path
for folder in os.listdir(path):

    # Go through each file in each folder
    for filename in os.listdir(path + "\\" + folder):

        # Finds shapefile
        if filename.endswith(".shp"):

            # Makes shapefile the current path
            newPath = path + "\\" + folder + "\\" + filename
            print(newPath)

            # Read and plot the shapefile
            city = geopandas.read_file(newPath)
            if filename == "natural.shp":
                axes = city.plot(edgecolors = "green", label = "natural")
            else:
                city.plot(ax = axes, label = "roads")

    else:
        continue

plt.show()
