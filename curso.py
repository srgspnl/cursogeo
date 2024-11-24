import geopandas as gpd
import folium
from folium import GeoJson
import streamlit as st

# Caminho do arquivo GeoJSON
geojson_file_path = "c:/Arquivos de Programas/python311/geojson/CursoDagua.geojson"

# Carregar o arquivo GeoJSON
try:
    # Carregar o arquivo GeoJSON com dados dos rios
    gdf = gpd.read_file(geojson_file_path)

    # Verificar se a coluna 'noriocomp' existe
    if 'noriocomp' in gdf.columns:
        # Obter a lista de nomes únicos de rios
        nomes_rios = gdf['noriocomp'].dropna().unique()

        # Barra de seleção para o usuário escolher um rio
        rio_escolhido = st.selectbox("Escolha o rio para visualização:", sorted(nomes_rios))

        # Filtrar o GeoDataFrame para o rio selecionado
        rio_selecionado = gdf[gdf['noriocomp'] == rio_escolhido]

        # Verificar se o filtro retornou algum dado
        if not rio_selecionado.empty:
            st.write(f"Visualizando o curso do rio: **{rio_escolhido}**")

            # Reprojetar o curso do rio para WGS84 (EPSG:4326) e obter os limites
            rio_selecionado = rio_selecionado.to_crs("EPSG:4326")
            bounds = rio_selecionado.total_bounds  # [minx, miny, maxx, maxy]
            center_lat = (bounds[1] + bounds[3]) / 2  # Latitude média
            center_lon = (bounds[0] + bounds[2]) / 2  # Longitude média

            # Ajustar zoom proporcional ao curso do rio (usando o tamanho dos limites)
            zoom_start = 10 if (bounds[2] - bounds[0]) < 0.5 else 8

            # Criar o mapa base centrado nos limites do rio
            mapa = folium.Map(location=[center_lat, center_lon], zoom_start=zoom_start, tiles="OpenStreetMap")

            # Adicionar o curso do rio no mapa
            GeoJson(
                rio_selecionado.__geo_interface__,
                name=f"Curso do Rio: {rio_escolhido}",
                style_function=lambda x: {"color": "blue", "weight": 3},
            ).add_to(mapa)

            # Adicionar controle de camadas
            folium.LayerControl().add_to(mapa)

            # Exibir o mapa no Streamlit
            st.components.v1.html(mapa._repr_html_(), height=600)
        else:
            st.write("Nenhum dado encontrado para o rio selecionado.")
    else:
        st.write("A coluna 'noriocomp' não existe no arquivo GeoJSON.")
except Exception as e:
    st.write(f"Erro ao carregar ou processar o arquivo GeoJSON: {e}")
