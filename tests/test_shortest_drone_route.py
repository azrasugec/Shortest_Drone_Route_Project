import pytest
from projekodlari import shortest_drone_route

def test_download_map_data():
    graph, no_fly_zones = shortest_drone_route.download_map_data("Çankaya, Ankara, Turkey")
    assert graph is not None
    assert not no_fly_zones.empty

def test_compute_shortest_path():
    graph, _ = shortest_drone_route.download_map_data("Çankaya, Ankara, Turkey")
    origin = (39.911, 32.85)
    destination = (39.928, 32.86)
    route = shortest_drone_route.compute_shortest_path(graph, origin, destination)
    assert isinstance(route, list)
    assert len(route) > 0

def test_export_no_fly_zones_to_geojson(tmp_path):
    _, no_fly_zones = shortest_drone_route.download_map_data("Çankaya, Ankara, Turkey")
    output_file = tmp_path / "yasakli_bolgeler.geojson"
    shortest_drone_route.export_no_fly_zones_to_geojson(no_fly_zones, str(output_file))
    assert output_file.exists()

def test_export_route_to_geojson(tmp_path):
    graph, _ = shortest_drone_route.download_map_data("Çankaya, Ankara, Turkey")
    origin = (39.911, 32.85)
    destination = (39.928, 32.86)
    route = shortest_drone_route.compute_shortest_path(graph, origin, destination)
    output_file = tmp_path / "rota.geojson"
    shortest_drone_route.export_route_to_geojson(graph, route, str(output_file))
    assert output_file.exists()
