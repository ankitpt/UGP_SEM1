from shapely.geometry import Polygon
import pandas as pd

poly = Polygon(((0, 0), (0, 1), (1, 1), (1, 0)))

ndb=pd.read_csv("mobnet_processed_idea.csv")
