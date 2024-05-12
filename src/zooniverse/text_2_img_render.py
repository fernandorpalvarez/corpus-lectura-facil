import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from tqdm import tqdm


def df_2_imgs(base_path):
    """
    Takes a Dataframe given as input, takes each of the rows and saves its text into images
    """
    # Create a blank photo from scratch
    img = Image.new("RGBA", (1450, 150), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    arial_font = ImageFont.truetype("./Fonts/Arial-Unicode-Regular.ttf", 25)

    # Let's iterate over the phrases
    data_path = base_path + "extracted_text_pipeline/transformed/final_corpus.csv"
    # This is the initial position of the text in the image
    height = 65
    width = 55

    # Read the data
    text_df = pd.read_csv(data_path, sep="|")
    # Filter out "Lectura Fácil"
    text_df = text_df[text_df["class"] != 0]
    for index, phrase in tqdm(enumerate(text_df["text"])):
        draw.text((width, height), phrase, fill=(0, 0, 0), font=arial_font)
        img.save(base_path + f"zooniverse_data/subject_data/text_{index}.png")
        img = Image.new("RGBA", (1450, 150), (255, 255, 255))
        draw = ImageDraw.Draw(img)


if __name__ == '__main__':
    path = (
        "C:/Users/ferna/Universidad Politécnica de Madrid/Linea Accesibilidad Cognitiva (Proyecto)-Corpus Lectura "
        "Fácil (2023) - Documentos/data/")
    df_2_imgs(path)
