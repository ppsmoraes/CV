import json
import os
from fpdf import FPDF


class Curriculum:
    def __init__(self, filename=r'data/curriculum.json'):
        self.filename = filename
        self.data = self.load_data()

    def load_data(self) -> dict:
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                return json.load(file)
        return dict()

    def save_data(self) -> None:
        if not os.path.exists('data'):
            os.makedirs('data')
        with open(self.filename, 'w') as file:
            json.dump(self.data, file)

    def add_data(self, category: str, data: str, *, subcategory: str | bool = False) -> None:
        if not subcategory:
            if category not in self.data:
                self.data[category] = data
            else:
                if isinstance(self.data[category], str):
                    self.data[category] = [self.data[category]]
                self.data[category].append(data)
        else:
            if category not in self.data:
                self.data[category] = dict()
            if subcategory not in self.data[category]:
                self.data[category][subcategory] = data
            else:
                if isinstance(self.data[category][subcategory], str):
                    self.data[category][subcategory] = [self.data[category][subcategory]]
                self.data[category][subcategory].append(data)
        self.save_data()

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
            if subcategory in self.data['Contato']:
                if os.path.exists(rf'Images\{subcategory}.png'):
                    pdf.image(rf'Images\{subcategory}.png', x=5, y=pdf.get_y() + 2.5, h=5)  # y centraliza com o texto
                if use_link:
                    _font_style: str = 'U'
                    _color: tuple[int, int, int] = 1, 75, 160
                    _link: str = f'https://{self.data['Contato'].get(subcategory)}'
                else:
                    _font_style: str = ''
                    _color: tuple[int, int, int] = 0, 0, 0
                    _link: str = ''
                pdf.set_font('Helvetica', size=10, style=_font_style)
                pdf.set_text_color(*_color)
                pdf.cell(
                    largura_coluna,
                    10,
                    self.data['Contato'].get(subcategory),
                    ln=True,
                    link=_link,
                )

        if 'Contato' in self.data:
            pdf.set_y(60)  # Move para baixo da foto
            pdf.set_font('Helvetica', size=12, style='B')
            pdf.cell(largura_coluna, 10, 'Contato', ln=True, align='C')

            add_contato('Github', True)
            add_contato('Linkedin', True)
            add_contato('Email')
            add_contato('Telefone')

        # Corpo do currículo
        # -------------------------------------------------------------------------------
        # Nome
        pdf.set_y(pdf.t_margin)  # Topo da página
        pdf.set_x(60)  # Move para a direita
        pdf.set_text_color(0, 0, 0)
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

        # Tecnologias
        if 'Tecnologias' in self.data:
            print(f'Selecione as tecnologias para incluir no currículo:')
            for i, item in enumerate(self.data['Tecnologias']):
                print(f'{i + 1}. {item}')
            selected_indices = input(f'Digite os números das tecnologias em ordem (separados por vírgula): ').split(',')
            selected_indices = [index.strip() for index in selected_indices if index.strip()]
            if selected_indices:
                pdf.set_font('Helvetica', size=12, style='B')
                pdf.set_y(pdf.get_y() + 5)
                pdf.set_x(60)
                pdf.cell(140, 10, 'Tecnologias', ln=True)
                pdf.set_font('Helvetica', size=12)
                pdf.set_x(60)
                tecnologies = ', '.join([self.data['Tecnologias'][int(i) - 1] for i in selected_indices])
                pdf.cell(140, 10, tecnologies, ln=True)

        # Demais seções
        def write_section(section):
            if section in self.data:
                print(f'Selecione os(as) {section} para incluir no currículo:')
                for i, item in enumerate(self.data[section]):
                    print(f'{i + 1}. {item}')
                selected_indices = input(f'Digite os números dos(as) {section} (separados por vírgula): ').split(',')
                selected_indices = [index.strip() for index in selected_indices if index.strip()]
                if selected_indices:
                    pdf.set_font('Helvetica', size=12, style='B')
                    pdf.set_y(pdf.get_y() + 5)
                    pdf.set_x(60)
                    pdf.cell(140, 10, section, ln=True)
                    pdf.set_font('Helvetica', size=12)
                    for index in selected_indices:
                        pdf.set_x(60)
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

        choice = input('Escolha uma opção: ').strip()

        match choice:
            case '1':
                while True:
                    print('\nSubmenu "Adicionar dados":')
                    print(f'Categorias: {[key for key in curriculum.data.keys()]}')
                    print('Digite "back" para voltar para o menu principal')

                    category = input('Escolha uma categoria existente ou crie uma nova: ').strip()

                    match category:
                        case '':
                            print('Opção inválida! Tente novamente.')
                        case 'back':
                            break
                        case _:
                            while True:
                                print(f'\nSubmenu "Adicionar {category}":')
                                if category in curriculum.data:
                                    if isinstance(curriculum.data[category], str) or isinstance(
                                        curriculum.data[category], list
                                    ):
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
                                        print('Digite "back" para voltar para ao menu anterior')
                                        subcategory = input('Escolha uma subcategoria ou crie uma nova: ')
                                        match subcategory.strip():
                                            case 'back':
                                                break
                                            case _:
                                                data = input(f'Digite seu(a) {subcategory}: ')
                                                curriculum.add_data(
                                                    category,
                                                    data,
                                                    subcategory=subcategory,
                                                )
                                else:
                                    print('Digite "back" para voltar para ao menu anterior')
                                    add_subcategory = input(
                                        f'Deseja adicionar subcategorias para os(as) {category}? (S/N) '
                                    )
                                    match add_subcategory.lower():
                                        case 's':
                                            subcategory = input('Digite a nova subcategoria: ')
                                            match subcategory.strip():
                                                case 'back':
                                                    break
                                                case _:
                                                    data = input(f'Digite seu(a) {subcategory}: ')
                                                    curriculum.add_data(
                                                        category,
                                                        data,
                                                        subcategory=subcategory,
                                                    )
                                        case 'n':
                                            data = input(f'Digite seu(a) {category}: ')
                                            match data:
                                                case 'back':
                                                    break
                                                case _:
                                                    curriculum.add_data(category, data)
                                        case _:
                                            print('Opção inválida! Tente novamente.')
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
