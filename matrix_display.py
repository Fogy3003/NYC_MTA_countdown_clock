from rgbmatrix import RGBMatrix, RGBMatrixOptions


def init_matrix(self, rows=32, cols=64, chain_length=2, parallel=1, hardware_mapping="regular"):
    # Configure matrix options
    options = RGBMatrixOptions()
    options.rows = rows
    options.cols = cols
    options.chain_length = chain_length
    options.parallel = parallel
    options.hardware_mapping = hardware_mapping

    # Initialize the matrix
    matrix = RGBMatrix(options=options)
    return matrix
