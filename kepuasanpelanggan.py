import streamlit as st
import networkx as nx

# Membuat graph (graf) dengan NetworkX
G = nx.Graph()

# Tambahkan node (titik lokasi) dan edges (hubungan antar lokasi) dengan jarak
# Format: G.add_edge('titik1', 'titik2', weight=jarak)
G.add_edge('Warehouse', 'A', weight=10)
G.add_edge('Warehouse', 'B', weight=15)
G.add_edge('A', 'C', weight=10)
G.add_edge('B', 'C', weight=5)
G.add_edge('B', 'D', weight=10)
G.add_edge('C', 'D', weight=5)
G.add_edge('C', 'E', weight=15)
G.add_edge('D', 'E', weight=5)

# Fungsi untuk menghitung rute terpendek dengan Dijkstra
def shortest_route(start, end):
    # Dijkstra untuk menemukan rute terpendek
    length, path = nx.single_source_dijkstra(G, start)
    return path[end], length[end]

# Streamlit App
st.title('Optimasi Rute Pengiriman')

st.write("""
Aplikasi ini membantu mengoptimalkan rute pengiriman barang dari satu lokasi ke lokasi lain.
""")

start_location = st.selectbox('Pilih lokasi awal:', list(G.nodes))
end_location = st.selectbox('Pilih lokasi tujuan:', list(G.nodes))

if start_location != end_location:
    if st.button('Hitung Rute Terpendek'):
        try:
            path, distance = shortest_route(start_location, end_location)
            st.write(f"Rute Terpendek: {' -> '.join(path)}")
            st.write(f"Jarak total: {distance} km")
        except Exception as e:
            st.write("Error dalam menghitung rute:", str(e))
else:
    st.write("Pilih lokasi yang berbeda untuk menghitung rute.")
