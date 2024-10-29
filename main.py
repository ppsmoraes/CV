import json
import os
from fpdf import FPDF


class Curriculum:
    def __init__(self, filename=r'data\curriculum.json'):
        self.filename = filename
        self.data = self.load_data()

    def load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                return json.load(file)
        return dict()

    def save_data(self):
        if not os.path.exists('data'):
            os.makedirs('data')
        with open(self.filename, 'w') as file:
            json.dump(self.data, file)

    def add_data(self, category, data, *, subcategory=False):
        if not subcategory:
            if category not in self.data:
                self.data[category] = data
            else:
                self.data[category] = list(self.data[category])
                self.data[category].append(data)
        else:
            if category not in self.data:
                self.data[category] = dict()
            if subcategory not in self.data[category]:
                self.data[category][subcategory] = data
            else:
                self.data[category][subcategory] = list(self.data[category][subcategory])
                self.data[category][subcategory].append(data)
        self.save_data()

    def generate_pdf(self):
        pdf = FPDF()
        pdf.add_page()

        # Coluna destaque
        # -------------------------------------------------------------------------------
        pdf.set_fill_color(189, 236, 182)  # Definindo a cor de destaque
        pdf.rect(0, 0, 55, 297, 'F')  # (A4: 210x297 mm)

        # Foto
        if os.path.exists(r'Images\foto.png'):
            pdf.image(r'Images\foto.png', x=5, y=8, w=45)  # x, y e largura em mm

        largura_coluna = 55-2*pdf.l_margin
        pdf.set_y(60) # Move para baixo da foto
        pdf.set_font('Helvetica', size=12, style='B')
        pdf.cell(largura_coluna, 10, 'Contato', ln=True, align='C')

        def add_contato(subcategory, link=''):
            _font_style = ''
            _red = 0
            _green = 0
            _blue = 0
            if subcategory not in self.data['Contato']:
                raise f'{subcategory} não está nos dados de Contato.'
            if os.path.exists(rf'Images\{subcategory}.png'):
                pdf.image(rf'Images\{subcategory}.png', x=5, y=pdf.get_y()+2.5, h=5) # y centraliza com o texto
            if link == True:
                _font_style = 'U'
                _red = 1
                _green = 75
                _blue = 160
                link = f'https://{self.data['Contato'].get(subcategory)}'
            pdf.set_font('Helvetica', size=10, style=_font_style)
            pdf.set_text_color(_red, _green, _blue)
            pdf.cell(largura_coluna, 10, self.data['Contato'].get(subcategory), ln=True, link=link)

        if 'Contato' in self.data:
            add_contato('Github', True)
            add_contato('Linkedin', True)
            add_contato('Email')
            add_contato('Telefone')

        # Corpo do currículo
        # -------------------------------------------------------------------------------
        # Nome
        pdf.set_x(60)  # Move para a direita
        pdf.set_font('Helvetica', size=16, style='B')
        pdf.cell(140, 5, self.data.get('Nome', 'Fulano da Silva'), ln=True)

        # Vaga
        pdf.set_x(60)
        pdf.set_font('Helvetica', size=14)
        vaga = input('Para qual vaga esse currículo está sendo gerado? ')
        pdf.cell(140, 10, vaga, ln=True)

        # Resumo
        pdf.set_x(60)
        pdf.set_font('Helvetica', size=12)
        pdf.multi_cell(
            140,
            5,
            'Esse é um resumo. Aqui você deve deixar uma mensagem personalizada para cada currículo gerado baseado na vaga a qual esse currículo será aplicado.',
        )

        # TODO aqui deve ir as tecnologias

        def write_section(section):
            if section in self.data:
                print(f'Selecione os(as) {section} para incluir no currículo:')
                for i, item in enumerate(self.data[section]):
                    print(f'{i + 1}. {item}')
                selected_indices = input(f'Digite os números dos(as) {section} (separados por vírgula): ').split(',')
                selected_indices = [index.strip() for index in selected_indices if index.strip()]
                if selected_indices:
                    pdf.cell(140, 10, ln=True)  # Linha em branco
                    pdf.set_font('Helvetica', size=12, style='B')
                    pdf.cell(140, 10, section, ln=True)
                    pdf.set_font('Helvetica', size=12)
                    for index in selected_indices:
                        pdf.cell(200, 10, f'- {self.data[section][int(index) - 1]}', ln=True)

        write_section('Experiências')
        write_section('Idiomas')
        write_section('Cursos')

        pdf.output('curriculo.pdf')
        print('PDF gerado com sucesso!')


def main():
    curriculum = Curriculum()

    while True:
        print('\nMenu:')
        print('1. Adicionar dados')
        print('2. Gerar PDF e sair')
        print('3. Sair')

        choice = input('Escolha uma opção: ')

        match choice:
            case '1':
                while True:
                    print('\nSubmenu "Adicionar dados":')
                    print(f'Categorias: {[key for key in curriculum.data.keys()]}')
                    print('Digite "back" para voltar para o menu principal')

                    category = input('Escolha uma categoria existente ou crie uma nova: ')

                    match category:
                        case 'back':
                            break
                        case _:
                            while True:
                                print(f'\nSubmenu "Adicionar {category}":')
                                if category in curriculum.data:
                                    if isinstance(curriculum.data[category], str) or isinstance(curriculum.data[category], list):
                                        print(f'Dados: {curriculum.data[category]}')
                                        print('Digite "back" para voltar para ao menu anterior')
                                        data = input(f'Digite seu(a) {category}: ')
                                        match data:
                                            case 'back':
                                                break
                                            case _:
                                                curriculum.add_data(category, data)
                                    else:
                                        print(f'Subcategorias: {[key for key in curriculum.data[category]]}')
                                        print('Pressione enter para seguir sem subcategoria')
                                        print('Digite "back" para voltar para ao menu anterior')
                                        subcategory = input('Escolha uma subcategoria: ')
                                        match subcategory.strip():
                                            case '':
                                                data = input(f'Digite seu(a) {category}: ')
                                                curriculum.add_data(category, data)
                                            case 'back':
                                                break
                                            case _:
                                                data = input(f'Digite seu(a) {subcategory}: ')
                                                curriculum.add_data(category, data, subcategory=subcategory)
            case '2':
                curriculum.generate_pdf()
                print('Saindo...')
                break
            case '3':
                print('Saindo...')
                break
            case _:
                print('Opção inválida! Tente novamente.')


if __name__ == '__main__':
    main()
