import numpy as np
from monopoly.board import MonopolyBoard

def generate_data(board_data: MonopolyBoard, count: int, assets_scale: float):
    board_data.do_log = False

    asset_matrix = []
    board_before_matrix = []
    board_after_matrix = []
    for i in range(count):
        board_data.randomize()

        board_before_matrix.append(board_data.to_matrix(assets_scale=assets_scale))

        asset_before = np.array(board_data.assets)
        board_data.cycle()
        asset_after = np.array(board_data.assets)

        asset_matrix.append([(asset_after - asset_before) * assets_scale])
        board_after_matrix.append(board_data.to_matrix(assets_scale=assets_scale))

    board_data.do_log = True

    return asset_matrix, board_before_matrix, board_after_matrix
