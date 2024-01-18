from image_utils import get_image_properties, count_fully_transparent_pixels

def check_texture(texture_path):
    process = True
    texture_dimensions, texture_color_count = get_image_properties(texture_path)
    # check for fmv roughly
    if texture_color_count > 20000 and texture_dimensions[0] == 512 and texture_dimensions[1] == 512:
        print(texture_color_count)
        process = False

    # check for garbled font textures ?
    if texture_dimensions[0] == 512 and texture_dimensions[1] == 512 and process is True:
        tran = count_fully_transparent_pixels(texture_path)
        if tran > .90:
            process = False
    return process