import os
from PIL import Image
from pdf2image import convert_from_path


def get_files():
    print("Getting list of image files")
    files = os.listdir("./images")
    print(files)
    return files[1:-1]


def process_files(image_list):
    print("Splitting double-wide pages to single page")
    for i in image_list:
        page_a = ''
        page_b = ''
        img = "./images/" + i
        img = Image.open(img)
        width = img.size[0]
        height = img.size[1]
        box1 = (0, 0, width / 2, height)
        box2 = (width / 2, 0, width, height)
        img_a = img.crop(box1)
        img_b = img.crop(box2)
        page_a += "a_" + i
        page_b += "b_" + i
        img_a.save('./split/' + page_a)
        img_b.save('./split/' + page_b)


def pdf_to_images():
    print("Converting PDF to Images")
    original_file = os.listdir("./input")
    pages = convert_from_path("./input/"+original_file[-1])
    for i in range(len(pages)):
        pages[i].save('./images/page' + f"{i:02}" + '.jpg', 'JPEG')
    return original_file[-1]


def images_to_pdf(final_file):
    print("Compiling final pdf")
    original = os.listdir("./images")
    final_pages = [Image.open("./images/" + original[0])]
    for i in range(len(original)-1):
        if i != 0:
            final_pages.append(Image.open("./split/a_page"+f"{i:02}"+".jpg"))
            final_pages.append(Image.open("./split/b_page"+f"{i:02}"+".jpg"))

    final_pages.append(Image.open("./images/" + original[len(original)-1]))
    final_file = "./output/"+final_file
    final_pages[0].save(
        final_file, "PDF", resolution=100.0, save_all=True, append_images=final_pages[1:]
    )


def cleanup():
    images_folder = os.listdir("./images")
    split_folder = os.listdir("./split")
    for i in images_folder:
        os.remove("./images/"+i)

    for i in split_folder:
        os.remove("./split/"+i)


name = pdf_to_images()
images = get_files()
process_files(images)
images_to_pdf(name)
cleanup()
