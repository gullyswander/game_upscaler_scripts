import os
import subprocess
import importlib
from .utils import scan_directory_for_images, open_ignore_file, write_ignore_file


# Set important variables
UPSCALE_METADATA_PATH = 'V:\\pcsx2_texture_dump\\SLUS-21845\\upscale_metadata\\'
TEXTURE_DUMP_PATH = 'V:\\pcsx2_texture_dump\\SLUS-21845\\dumps\\'
TEXTURE_LOAD_PATH = 'V:\\pcsx2_texture_dump\\SLUS-21845\\replacements\\'
REAL_ESRGAN_PATH = 'V:\\realesrgan-ncnn-vulkan-20220424-windows\\realesrgan-ncnn-vulkan.exe'

#used for dynamic import
TEXTURE_FILTER_CODE = 'SLUS_21845'

#dynamically import code for game we care about
module_name = f'game_texture_code.{TEXTURE_FILTER_CODE}'
module = importlib.import_module(module_name)
# Retrieve the desired function from the imported module
check_texture = getattr(module, 'check_texture')


files_to_ignore = set()
def main():
    #setup some important tracking files
    textures_to_ignore_filepath = UPSCALE_METADATA_PATH + 'ignore.json'
    files_to_ignore = open_ignore_file(textures_to_ignore_filepath)

    while True:
        texture_files = scan_directory_for_images(TEXTURE_DUMP_PATH)
        upscaled_files = scan_directory_for_images(TEXTURE_LOAD_PATH)

        # Determine which textures have not yet been processed
        textures_to_process = []
        for texture_file in texture_files:
            add_file = True
            texture_f = texture_file.replace(TEXTURE_DUMP_PATH, TEXTURE_LOAD_PATH)
            if texture_f in upscaled_files:
                # print(f"already in upscaled: {texture_file}")
                add_file = False
            if texture_file in files_to_ignore:
                add_file = False

            if add_file is True:
                textures_to_process.append(texture_file)

        # Process the textures
        print("*" * 80)
        print(f'textures to process:{len(textures_to_process)} ')
        i = 1
        for texture_path in textures_to_process:
            try:
                print(f'completed: {i}/{len(textures_to_process)} ')
                i += 1
                process = check_texture(texture_path)

                if process is False:
                    print(f"ignoring : {texture_path}")
                    files_to_ignore.add(texture_path)

                if process == True:
                    print(f"Processing texture: {texture_path}")
                    output_path = texture_path.replace(TEXTURE_DUMP_PATH, TEXTURE_LOAD_PATH)
                    command = [
                        f'{REAL_ESRGAN_PATH}',
                        '-i', texture_path,
                        '-s', '3',
                        '-o', output_path,
                        "j", "4:4:4"
                    ]
                    print(command)
                    subprocess.call(command)
                    print(f"completed: {texture_path}")
            except Exception as e:
                print(e)
        write_ignore_file(textures_to_ignore_filepath,files_to_ignore)


if __name__ == "__main__":
    main()





