import ee
import ipyleaflet


def mapping(center: tuple = (40, -100), zoom: int = 4, layers=None) -> ipyleaflet.Map:
    """
    membuat peta interaktif menggunakan ipyleaflet

    Parameter:
        - center (tuple): koordinat pusat awal peta, default adalah (40, -100)
        - zoom (int): menentukan tingkat zoom awal peta, default adalah 4
        - layers: layer tambahan yang akan ditambahkan ke peta, bisa berupa satu alayer atau daftar layer

    Return:
        ipyleaflet.Map: objek peta ipyleaflet dengan parameter yang sudah ditentukan

    Contoh:
    >>> mapping(center=(34, -118), zoom=8)
    """
    # membuat objek peta dengan parameter yang sudah diberikan
    m = ipyleaflet.Map(center=center, zoom=zoom)
    # menambahkan kontrol layer pada sudut kanan atas
    m.add_control(ipyleaflet.LayersControl(position="topright"))
    # menambahkan kontrol layer pada sudut kiri bawah
    m.add_control(ipyleaflet.ScaleControl(position="bottomleft"))
    # menambahkan kontrol layar penuh
    m.add_control(ipyleaflet.FullScreenControl())
    # menambahkan kontrol gambar
    m.add_control(ipyleaflet.DrawControl())

    # menambahkan kontrol pengukuran pada sudut kiri bawah
    measure = ipyleaflet.MeasureControl(
        position="bottomleft", active_color="orange", primary_length_unit="kilometers"
    )
    m.add_control(measure)

    # mengecek apakah layer adalah None atau tidak
    if layers is None:
        # joka none menambahkan layer peta google Satellite
        tile_layer = ipyleaflet.TileLayer(
            url="https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}",
            attribute="Google",
            name="Google Satellite",
        )
        m.add_layer(tile_layer)
    else:
        # jika tidak, menambahkan layer yang diberikan
        m.add_layer(layers)
    return m


def add_layer(
    self, ee_object, vis_params={}, name="Layer untitled", shown=True, opacity=1
):
    """
    Menambahkan layer ke peta menggunakan objek Google Earth Engine (GEE).

    Parameters:
        - self: Objek peta ipyleaflet yang akan ditambahkan layer.
        - ee_object: Objek GEE yang akan ditampilkan sebagai layer.
        - vis_params (dict): Parameter visualisasi layer, contoh: {"bands": ['B4', 'B3', 'B2']}.
        - name (str): Nama layer yang ditampilkan pada peta. Default adalah "Layer tanpa judul".
        - shown (bool): Menentukan apakah layer ditampilkan secara default atau tidak. Default adalah True.
        - opacity (float): Tingkat opacity layer pada peta (0-1). Default adalah 1.

    Raises:
        - AttributeError: Jika objek ee_object tidak sesuai dengan tipe data yang diizinkan.

    Example:
        >>> peta = ipyleaflet.Map()
        >>> peta.add_layer(ee_object, vis_params={"bands": ['B4', 'B3', 'B2']}, name="Layer Landsat")
    """
    image = None

    # mengecek tipe data object GEE yang valid
    if (
        not isinstance(ee_object, ee.Image)
        and not isinstance(ee_object, ee.ImageCollection)
        and not isinstance(ee_object, ee.FeatureCollection)
        and not isinstance(ee_object, ee.Feature)
        and not isinstance(ee_object, ee.Geometry)
    ):
        err_str = "\n\nArgumen gambar pada fungsi 'add_layer' harus berupa instance dari ee.Image, ee.Geometry, ee.Feature, atau ee.FeatureCollection."
        raise AttributeError(err_str)

    # menentukan jenis object dan membuat layer sesuai dengan tipe object GEE
    if (
        isinstance(ee_object, ee.geometry.Geometry)
        or isinstance(ee_object, ee.feature.Feature)
        or isinstance(ee_object, ee.featurecollection.FeatureCollection)
    ):
        features = ee.FeatureCollection(ee_object)

        width = 2

        if "width" in vis_params:
            width = vis_params["width"]

        color = "000000"

        if "color" in vis_params:
            color = vis_params["color"]

        # menyusun layer dengan menggabungkan area dan garis batas objek
        image_fill = features.style(**{"fillColor": color}).updateMask(
            ee.Image.constant(0.5)
        )
        image_outline = features.style(
            **{"color": color, "fillColor": "00000000", "width": width}
        )

        image = image_fill.blend(image_outline)
    elif isinstance(ee_object, ee.image.Image):
        image = ee_object
    elif isinstance(ee_object, ee.imagecollection.ImageCollection):
        # mengambil nilai median dari koleksi model gambar
        image = ee_object.median()

    # get map ID dari object gambar EE
    map_id_dict = ee.Image(image).getMapId(vis_params)
    tile_layer = ipyleaflet.TileLayer(
        url=map_id_dict["tile_fetcher"].url_format,
        attribution="Google Earth Engine",
        name=name,
        opacity=opacity,
        visible=shown,
    )
    # menambahkan layer ke object peta
    self.add_layer(tile_layer)


ipyleaflet.Map.addLayer = add_layer


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


ipyleaflet.Map.setCenter = set_center


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


ipyleaflet.Map.centerObject = center_object


def add_wms_tile_layer(
    self,
    url,
    layers,
    name=None,
    attribution="",
    format="image/jpeg",
    transparent=False,
    opacity=1.0,
):
    """
    Menambahkan layer dari Web Map Service (WMS) ke peta.

    Parameter:
        - self: Objek peta ipyleaflet yang akan ditambahkan layer.
        - url (str): URL WMS service.
        - layers (str): Nama layer WMS yang akan ditampilkan.
        - nama (str): Nama layer yang ditampilkan pada peta. Jika tidak ditentukan, menggunakan nama layer WMS.
        - atribusi (str): Informasi atribusi layer.
        - format (str): Format gambar yang diinginkan (contoh: "image/jpeg").
        - transparan (bool): Menentukan apakah layer transparan atau tidak.
        - opacity(float): Tingkat opacity layer pada peta (0-1).

    Example:
        >>> peta = ipyleaflet.Map()
        >>> peta.tambahkan_layer_wms_tile(
        ...     url="https://example.com/wms",
        ...     layers="layer1",
        ...     nama="Layer WMS",
        ...     atribusi="Sumber Data",
        ...     format="image/png",
        ...     transparan=True,
        ...     opacity=0.8
        ... )
    """
    # jika nama tidak ditentukan, gunakan nama layer WMS
    if name is None:
        name = str(layers)
    try:
        # membuat object WMSLayer dan menambahkan ke peta
        wms_layer = ipyleaflet.WMSLayer(
            url=url,
            layers=layers,
            name=name,
            attribution=attribution,
            format=format,
            transparent=transparent,
            opacity=opacity,
        )
        self.add_layer(wms_layer)
    except Exception:
        print("error WMS tile layer")


ipyleaflet.Map.addWmsTileLayer = add_wms_tile_layer


def addTileLayer(
    self,
    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    name=None,
    attribute="",
    opacity=1,
):
    """
    Menambahkan layer tile ke peta.

    Parameter:
        - self: Objek peta ipyleaflet yang akan ditambahkan layer.
        - url (str): URL tile layer (contoh: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png").
        - nama (str): Nama layer yang ditampilkan pada peta. Jika tidak ditentukan, menggunakan URL sebagai nama.
        - atribusi (str): Informasi atribusi layer.
        - opacity (float): Tingkat opacity layer pada peta (0-1).

    Example:
        >>> peta = ipyleaflet.Map()
        >>> peta.tambahkan_layer_tile(
        ...     url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        ...     nama="OpenStreetMap",
        ...     atribusi="OpenStreetMap Contributors",
        ...     opacity=0.9
        ... )
    """
    try:
        tile_layer = ipyleaflet.TileLayer(
            url=url, name=name, attribution=attribute, opacity=opacity
        )
        self.add_layer(tile_layer)
    except Exception:
        print("failed tile layer")


ipyleaflet.Map.addTileLayer = addTileLayer

if __name__ == "__main__":
    map = mapping()
    print(map)
