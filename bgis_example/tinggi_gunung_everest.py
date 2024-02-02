from bgis import bgis
import ee

try:
    ee.Initialize()
except Exception:
    ee.Authenticate()
    ee.Initialize(project="ee-bellshade")

Map = bgis.mapping()

image_dataset = ee.Image("USGS/SRTMGL1_003")
xy = ee.Geometry.Point([86.9250, 27.9881])
elev = image_dataset.sample(xy, 30).first().get("elevation").getInfo()
print(f"Ketinggian elevasi dari mount everest (secara detail) adalah: {elev} meter")
