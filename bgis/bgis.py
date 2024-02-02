import ipyleaflet
import bgis.map.layer_map as layer_map
import bgis.map.object_map as object_map


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


ipyleaflet.Map.addLayer = layer_map.add_layer
ipyleaflet.Map.setCenter = object_map.set_center
ipyleaflet.Map.centerObject = object_map.center_object
ipyleaflet.Map.addWmsTileLayer = layer_map.add_wms_tile_layer
ipyleaflet.Map.addTileLayer = layer_map.add_wms_tile_layer
ipyleaflet.Map.listening = object_map.listening
ipyleaflet.Map.last_click = []
ipyleaflet.Map.all_clicks = []

if __name__ == "__main__":
    map = mapping()
    print(map)
