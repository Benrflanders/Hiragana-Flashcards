from fpdf import FPDF
from pykakasi import kakasi

hiragana_chars = ['あ', 'い', 'う', 'え', 'お', 
                  'か', 'き', 'く', 'け', 'こ',
                  'さ', 'し', 'す', 'せ', 'そ', 
                  'た', 'ち', 'つ', 'て', 'と', 
                  'な', 'に', 'ぬ', 'ね', 'の', 
                  'は', 'ひ', 'ふ', 'へ', 'ほ', 
                  'ま', 'み', 'む', 'め', 'も', 
                  'や', 'ゆ', 'よ', 
                  'ら', 'り', 'る', 'れ', 'ろ', 
                  'わ', 'を', 'ん']

def dashed_line(pdf, x1, y1, x2, y2, dash_length = 1, space_length = 1):
    dash_gap = dash_length + space_length
    x_var = x2 - x1
    y_var = y2 - y1
    length = ((x_var**2)+(y_var**2))**0.5
    dash_count = int(length / dash_gap)
    
    for i in range(dash_count):
        x_start = x1 + ((i / dash_count) * x_var)
        y_start = y1 + ((i / dash_count) * y_var)
        x_end = x1 + (((i + dash_length) / dash_count) * x_var)
        y_end = y1 + (((i + dash_length) / dash_count) * y_var)
        pdf.line(x_start, y_start, x_end, y_end)


def generate_pdf(filename, data, font_name, font_file, font_size=36, x_offset=10, y_offset=10, card_width=85, card_height=55):
    pdf = FPDF(orientation='P', unit='mm', format='A4')

    # Add Unicode font
    pdf.add_font(font_name, fname=font_file, uni=True)
    
    pdf.add_page()
    pdf.set_font(font_name, size = font_size)
    
    x, y = x_offset, y_offset
    for character in data:
        pdf.set_xy(x, y)
        pdf.cell(card_width, card_height, txt = character, align='C')
        dashed_line(pdf, x, y, x+card_width, y)  # top
        dashed_line(pdf, x, y, x, y+card_height)  # left
        dashed_line(pdf, x+card_width, y, x+card_width, y+card_height)  # right
        dashed_line(pdf, x, y+card_height, x+card_width, y+card_height)  # bottom

        x += card_width + x_offset
        if x > 210 - card_width:  # 210mm is an A4 page width
            x = x_offset
            y += card_height + y_offset
            if y > 297 - card_height:  # 297mm is an A4 page height
                y = y_offset
                pdf.add_page()
    pdf.output(filename)

def hiragana_to_romaji(hiragana_chars):
    kakasi_instance = kakasi()
    kakasi_instance.setMode('H', 'a')  # Hiragana to ascii
    conv = kakasi_instance.getConverter()
    return [conv.do(char) for char in hiragana_chars]

def main():
    romaji_chars = hiragana_to_romaji(hiragana_chars)

    # Change this to the location of DejaVuSans.ttf on your system
    font_file = './NotoSansJP-Regular.ttf'  

    generate_pdf("hiragana.pdf", hiragana_chars, 'NotoSansJP', font_file)
    generate_pdf("romaji.pdf", romaji_chars, 'NotoSansJP', font_file)

if __name__ == "__main__":
    main()