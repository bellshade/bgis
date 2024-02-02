import ee
import ipyleaflet


def set_center(self, lon, lat, zoom=None):
    """
    Mengatur pusat dan zoom level pada peta.

    Parameter:
        - self: Objek peta ipyleaflet yang akan diatur pusat dan zoom levelnya.
        - lon (float): Koordinat longitude untuk pusat peta.
        - lat (float): Koordinat latitude untuk pusat peta.
        - zoom (int): Tingkat zoom yang diinginkan. Jika tidak ditentukan, zoom level tidak diubah.
    """
    # mengatur pusat peta dengan koordinat yang diberikan
    self.center = (lat, lon)
    # mengatur tingkat zoom jika diberikan
    if zoom is not None:
        self.zoom = zoom


def center_object(self, ee_object, zoom=None):
    """
    Memusatkan peta pada objek Google Earth Engine (GEE) dan dapat mengatur tingkat zoom.

    Parameter:
        - self: Objek peta ipyleaflet yang akan diatur pusatnya.
        - objek_gee: Objek GEE yang akan dijadikan pusat peta.
        - zoom (int): Tingkat zoom yang diinginkan. Jika tidak ditentukan, zoom level tidak diubah.
    """
    # koordinat awal pusat dan batas peta
    lat = 0
    lon = 0

    # menetukan koordinat pusat dan batas peta berdasarkan jenis object GEE
    if isinstance(ee_object, ee.geometry.Geometry):
        centroid = ee_object.centroid()
        lon, lat = centroid.getInfo()["coordinates"]
    elif isinstance(ee_object, ee.featurecollection.FeatureCollection):
        centroid = ee_object.geometry().centroid()
        lon, lat = centroid.getInfo()["coordinates"]
    elif isinstance(ee_object, ee.image.Image):
        geometry = ee_object.geometry()
        coordinates = geometry.getInfo()["coordinates"][0]
        lon, lat = coordinates[0][::-1], coordinates[2][::-1]
    elif isinstance(ee_object, ee.imagecollection.ImageCollection):
        geometry = ee_object.geometry()
        coordinates = geometry.getInfo()["coordinates"][0]
        lon, lat = coordinates[0][::-1], coordinates[2][::-1]

    # mengature pusat peta dengan koordinat yang didapatkan dan dapat mengatur tingkat zoom jika diberikan
    self.setCenter(lon, lat, zoom)


def listening(self, event: str = "click", add_marker: bool = True) -> None:
    """
    Memantau interaksi pengguna pada peta, seperti klik atau pergerakan mouse.

    Parameter:
        - self: Objek peta ipyleaflet yang akan dimonitor interaksinya.
        - event (str): Jenis interaksi yang akan dipantau, misalnya "click" atau "mousemove".
        - tambahkan_marker (bool): Menentukan apakah menambahkan penanda (marker) pada lokasi klik atau tidak.

    Contoh:
        >>> peta = ipyleaflet.Map()
        >>> peta.mendengarkan(event="click", tambahkan_marker=True)
    """
    koordinat = []

    def handle_interactive(**kwargs):
        latlon = kwargs.get("coordinates")

        if event == "click" and kwargs.get("type") == "click":
            koordinat.append(latlon)
            self.last_click = latlon
            self.all_click = latlon
            if add_marker:
                self.add_layer(ipyleaflet.Marker(location=latlon))
        elif kwargs.get("type") == "mousemove":
            pass

    self.on_interaction(handle_interactive)
