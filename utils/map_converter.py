import os

def convert_map_to_graph(filepath):
    """
    Moving AI Lab의 .map 파일을 읽어와서 지정된 형식의 그래프 딕셔너리로 변환합니다.

    Args:
        filepath (str): 변환할 .map 파일의 경로.

    Returns:
        dict: 사용자의 CBS 알고리즘에서 사용할 수 있는 형식의 그래프.
              (x, y): [((neighbor_x, neighbor_y), cost)]
              존재하지 않는 파일이거나 맵 데이터가 없으면 None을 반환합니다.
    """
    if not os.path.exists(filepath):
        print(f"오류: 파일을 찾을 수 없습니다 - {filepath}")
        return None

    with open(filepath, 'r') as f:
        lines = f.readlines()

    # 맵 데이터의 시작점을 찾습니다. 'map'이라는 단어 바로 다음 줄부터 시작합니다.
    try:
        map_start_index = lines.index('map\n') + 1
        map_lines = lines[map_start_index:]
    except ValueError:
        print("오류: .map 파일 형식이 올바르지 않습니다. 'map' 키워드를 찾을 수 없습니다.")
        return None

    height = len(map_lines)
    if height == 0:
        print("오류: 맵 데이터가 비어있습니다.")
        return None
    width = len(map_lines[0].strip())

    graph = {}
    # 이동 가능한 지형을 정의합니다. 필요에 따라 다른 문자를 추가할 수 있습니다.
    walkable_terrain = ['.', 'G', 'S', 'T']

    # 맵의 모든 셀을 순회합니다.
    for y, line in enumerate(map_lines):
        for x, char in enumerate(line.strip()):
            # 현재 셀이 이동 가능한 지형인 경우에만 그래프에 노드로 추가합니다.
            if char in walkable_terrain:
                neighbors = []
                # 상, 하, 좌, 우 4방향의 인접 셀을 확인합니다.
                for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                    nx, ny = x + dx, y + dy

                    # 인접 셀이 맵 경계 내에 있는지 확인합니다.
                    if 0 <= nx < width and 0 <= ny < height:
                        # 인접 셀이 이동 가능한 지형인지 확인합니다.
                        if map_lines[ny][nx] in walkable_terrain:
                            # 이동 비용은 1로 고정합니다.
                            cost = 1
                            neighbors.append(((nx, ny), cost))
                
                # 그래프에 현재 노드와 인접 노드 정보를 추가합니다.
                # 좌표는 (x, y) 형식으로 저장합니다.
                graph[(x, y)] = neighbors

    return graph

# --- 사용 예시 ---
if __name__ == '__main__':
    # 1. 여기에 변환하고 싶은 실제 .map 파일의 이름을 입력하세요.
    map_filename_to_convert = "warehouse-20-40-10-2-1.map" 
    
    # 2. 결과를 저장할 파일 이름을 정합니다.
    output_filename = "converted_graph.txt"

    # 3. 변환 함수를 호출합니다.
    my_graph = convert_map_to_graph(map_filename_to_convert)

    # 4. 결과를 터미널 대신 파일에 저장합니다.
    if my_graph:
        with open(output_filename, 'w') as f:
            for node, neighbors in my_graph.items():
                f.write(f"{node}: {neighbors}\n") # .write()를 사용하고 줄바꿈(\n)을 추가
        
        print(f"--- '{map_filename_to_convert}' 맵 변환 완료 ---")
        print(f"결과가 '{output_filename}' 파일에 저장되었습니다.")
        print(f"총 {len(my_graph)}개의 노드가 그래프로 변환되었습니다.")
