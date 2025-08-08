import json
import os
from fpdf import FPDF

class Curriculum:
    def __init__(self, filename=r'data/english.json'):
        self.filename = filename
        self.data = self.load_data()

    def load_data(self) -> dict:
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                return json.load(file)
        return dict()

    def generate_pdf(self) -> None:
        pdf: FPDF = FPDF()
        pdf.add_page()

        # Coluna destaque
        # -------------------------------------------------------------------------------
        pdf.set_fill_color(189, 236, 182)  # Definindo a cor de destaque
        pdf.rect(0, 0, 55, 297, 'F')  # (A4: 210x297 mm)

        # Foto
        if os.path.exists(r'Images\foto.png'):
            pdf.image(r'Images\foto.png', x=5, y=8, w=45)  # x, y e largura em mm

        largura_coluna: float = 55 - 2 * pdf.l_margin

        def add_contato(subcategory: str, use_link: bool = False):
            if subcategory in self.data['Contact']:
                if os.path.exists(rf'Images\{subcategory}.png'):
                    pdf.image(rf'Images\{subcategory}.png', x=5, y=pdf.get_y() + 2.5, h=5)  # y centraliza com o texto
                if use_link:
                    _font_style: str = 'U'
                    _color: tuple[int, int, int] = 1, 75, 160
                    _link: str = f'https://{self.data['Contact'].get(subcategory)}'
                else:
                    _font_style: str = ''
                    _color: tuple[int, int, int] = 0, 0, 0
                    _link: str = ''
                pdf.set_font('Helvetica', size=10, style=_font_style)
                pdf.set_text_color(*_color)
                pdf.cell(
                    largura_coluna,
                    10,
                    self.data['Contact'].get(subcategory),
                    ln=True,
                    link=_link,
                )

        if 'Contact' in self.data:
            pdf.set_y(60)  # Move para baixo da foto
            pdf.set_font('Helvetica', size=12, style='B')
            pdf.cell(largura_coluna, 10, 'Contact', ln=True, align='C')

            add_contato('Github', True)
            add_contato('Linkedin', True)
            add_contato('Email')
            add_contato('Phone')

        # Corpo do currículo
        # -------------------------------------------------------------------------------
        # Name
        pdf.set_y(pdf.t_margin)  # Topo da página
        pdf.set_x(60)  # Move para a direita
        pdf.set_text_color(0, 0, 0)
        pdf.set_font('Helvetica', size=16, style='B')
        pdf.cell(140, 5, self.data.get('Name', 'John Doe'), ln=True)

        # Position
        pdf.set_x(60)
        pdf.set_font('Helvetica', size=14)
        vaga = input('What the name of the desired position? ')
        pdf.cell(140, 10, vaga, ln=True)

        # Summary
        pdf.set_x(60)
        pdf.set_font('Helvetica', size=10)
        pdf.multi_cell(140, 5, self.data['Summary'])

        # Technologies
        if 'Technologies' in self.data:
            print(f'Select the technologies:')
            id_tec = {i + 1: item for i, item in enumerate(self.data['Technologies'])}
            for key, value in id_tec.items():
                print(f'{key}. {value}')
            selected_indices = input(f'Type the number in order (comma separeted): ').split(
                ','
            )
            selected_indices = [int(index.strip()) for index in selected_indices if index.strip()]
            if selected_indices:
                pdf.set_font('Helvetica', size=12, style='B')
                pdf.set_y(pdf.get_y() + 5)
                pdf.set_x(60)
                pdf.cell(140, 5, 'Technologies', ln=True)
                pdf.set_font('Helvetica', size=12)
                pdf.set_x(60)
                tecnologies = ', '.join([id_tec[i] for i in selected_indices])
                pdf.cell(140, 10, tecnologies, ln=True)

        # Experience
        if 'Experience' in self.data:
            print(f'Select the experiencies:')
            id_xp = {i + 1: item for i, item in enumerate(self.data['Experience'])}
            for key, value in id_xp.items():
                print(f'{key}. {value}')
            selected_indices = input(f'Type the number in order (comma separeted): ').split(',')
            selected_indices = [int(index.strip()) for index in selected_indices if index.strip()]
            if selected_indices:
                pdf.set_y(pdf.get_y() + 5)
                pdf.set_x(60)
                pdf.set_font('Helvetica', size=12, style='B')
                pdf.cell(140, 5, 'Experience', ln=True)
                for index in selected_indices:
                    pdf.set_x(60)
                    pdf.set_font('Helvetica', size=12)
                    pdf.cell(140, 5, self.data['Experience'][id_xp[index]]['Title'], ln=True)
                    pdf.set_x(60)
                    pdf.set_font('Helvetica', size=12, style='I')
                    pdf.cell(
                        140,
                        5,
                        f'{self.data['Experience'][id_xp[index]]['Period']} - {self.data['Experience'][id_xp[index]]['Company']}',
                        ln=True,
                    )
                    pdf.set_x(60)
                    pdf.set_font('Helvetica', size=10)
                    pdf.multi_cell(140, 5, self.data['Experience'][id_xp[index]]['Summary'])
                    pdf.set_y(pdf.get_y() + 5)

        # Languages
        if 'Languages' in self.data:
            print('Select the languages:')
            id_language = {i + 1: item for i, item in enumerate(self.data['Languages'])}
            for key, value in id_language.items():
                print(f'{key}. {value}')
            selected_indices = input('Type the number in order (comma separeted): ').split(',')
            selected_indices = [int(index.strip()) for index in selected_indices if index.strip()]
            if selected_indices:
                pdf.set_font('Helvetica', size=12, style='B')
                pdf.set_y(pdf.get_y() + 5)
                pdf.set_x(60)
                pdf.cell(140, 5, 'Languages', ln=True)
                for index in selected_indices:
                    pdf.set_font('Helvetica', size=12)
                    pdf.set_x(60)
                    pdf.cell(140, 10, f'- {id_language[index]}', ln=True)

        # Education
        if 'Education' in self.data:
            print('Select the courses: ')
            id_course = {i + 1: item for i, item in enumerate(self.data['Education'])}
            for key, value in id_course.items():
                print(f'{key}. {value}')
            selected_indices = input('Type the number in order (comma separeted): : ').split(',')
            selected_indices = [int(index.strip()) for index in selected_indices if index.strip()]
            if selected_indices:
                pdf.set_font('Helvetica', size=12, style='B')
                pdf.set_y(pdf.get_y() + 5)
                pdf.set_x(60)
                pdf.cell(140, 5, 'Education', ln=True)
                for index in selected_indices:
                    pdf.set_font('Helvetica', size=12)
                    pdf.set_x(60)
                    pdf.cell(140, 5, id_course[index], ln=True)
                    pdf.set_font('Helvetica', size=12, style='I')
                    pdf.set_x(60)
                    pdf.cell(140, 10, self.data['Education'][id_course[index]], ln=True)
                    pdf.set_y(pdf.get_y() + 5)

        pdf.output('Pablo_Moraes_CV.pdf')
        print('PDF generated with sucess!')

def main():
    curriculum = Curriculum()
    curriculum.generate_pdf()


if __name__ == '__main__':
    main()
