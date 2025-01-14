from PIL import Image

def rotate_image(image_path):
    image = Image.open(image_path)
    width, height = image.size

    if width < height:
        rotated_image = image.rotate(90, expand=True)
        rotated_image.save(image_path)
        print("已旋转图片！")
    else:
        print("这张图片的宽度不小于高度，不需要旋转。")

# 替换为你想要判断的图片路径
image_path = "E:\\Download\\flipermag-2024-12-09_08-06-31_004556-scaled.jpg"

rotate_image(image_path)
