import os
import osmnx as ox
import geopandas as gpd
import matplotlib.pyplot as plt
import networkx as nx

def download_map_data(place_name="Çankaya, Ankara, Turkey"):
    graph = ox.graph_from_place(place_name, network_type="drive")

    tags = {
        "landuse": "military",
        "aeroway": ["aerodrome", "runway"],
        "amenity": ["prison", "school", "kindergarten"],
        "leisure": "nature_reserve",
        "building": "government"
    }

    no_fly_zones = ox.features_from_place(place_name, tags)
    return graph, no_fly_zones

def plot_map(graph, no_fly_zones):
    fig, ax = ox.plot_graph(graph, show=False, close=False)
    no_fly_zones.plot(ax=ax, facecolor="red", alpha=0.5)
    plt.title("Yol Ağı ve Uçuşa Yasak Bölgeler (Çankaya)")
    plt.show()

def export_no_fly_zones_to_geojson(gdf, filename="export/yasakli_bolgeler.geojson"):
    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        gdf.to_file(filename, driver='GeoJSON')
        print(f"✅ GeoJSON dosyası kaydedildi: {filename}")
    except PermissionError:
        print("❌ Dosya başka bir uygulamada açık. Kapatıp tekrar deneyin.")

def compute_shortest_path(graph, origin_point, destination_point):
    orig_node = ox.nearest_nodes(graph, origin_point[1], origin_point[0])
    dest_node = ox.nearest_nodes(graph, destination_point[1], destination_point[0])

    route = nx.shortest_path(graph, orig_node, dest_node, weight='length')
    return route

def plot_route(graph, route, no_fly_zones):
    fig, ax = ox.plot_graph_route(graph, route, route_color='blue', show=False, close=False)
    no_fly_zones.plot(ax=ax, facecolor="red", alpha=0.5)
    plt.title("Drone Rotalı Harita")
    plt.show()

def export_route_to_geojson(graph, route, filename="export/rota.geojson"):
    try:
        if not route:
            print("⚠️ Rota verisi boş. Dosya yazılmadı.")
            return

        route_nodes = graph.subgraph(route)
        gdf_edges = ox.graph_to_gdfs(route_nodes, nodes=False)
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        gdf_edges.to_file(filename, driver="GeoJSON")
        print(f"✅ Rota GeoJSON dosyası kaydedildi: {filename}")
    except Exception as e:
        print(f"❌ Dosya yazılamadı! Hata: {e}")

if __name__ == "__main__":
    graph, no_fly_zones = download_map_data("Çankaya, Ankara, Turkey")
    export_no_fly_zones_to_geojson(no_fly_zones, "export/yasakli_bolgeler.geojson")

    origin = (39.911, 32.85)
    destination = (39.928, 32.86)

    route = compute_shortest_path(graph, origin, destination)

    # 🔍 Rota kontrol
    print("Rota uzunluğu:", len(route))
    print("Rota nodları:", route)

    plot_route(graph, route, no_fly_zones)
    export_route_to_geojson(graph, route, "export/rota.geojson")
