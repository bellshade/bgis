import ee
import ipyleaflet


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

    Contoh:
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

    Contoh:
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


def add_tile_layer(
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

    Contoh:
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
