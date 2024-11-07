import json
import os
from fpdf import FPDF


class Curriculum:
    def __init__(self, filename=os.path.join('data', 'curriculum.json')):
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
            json.dump(self.data, file, indent=4)

    def add_data(self):

        def add_level(data, level='Raiz'):

            def check_n_update(key, data, new_value):
                if key in data:
                    if isinstance(data[key], dict):
                        if isinstance(new_value, dict):
                            data[key] = new_value
                        else:
                            data[key][new_value] = []
                    elif isinstance(data[key], list):
                        data[key].append(new_value)
                    else:
                        data[key] = [data[key], new_value]
                else:
                    data[key] = new_value

            while True:
                print(f'\nVocê está no nível: {level}')
                if data:
                    print('Valores atuais nesta chave:')
                    if isinstance(data, dict):
                        for k, v in data.items():
                            print(f'  {k}: {v}')
                    else:
                        print(data)

                key = input(f'Digite a chave para {level} (ou "sair" para finalizar): ')

                if key.lower() == 'sair':
                    break

                value = input(f'Digite o valor para {key} (ou "objeto" para adicionar um novo nível): ')
                if value.lower() == 'objeto':
                    # Cria um novo dicionário para o próximo nível
                    if key in data:
                        if isinstance(data[key], dict):
                            new_dict = data[key]
                        else:
                            print(
                                '\033[93m'
                                + 'Não podemos adicionar um novo nível em um objeto com valores finais.'
                                + '\033[0m'
                            )
                            break
                    else:
                        new_dict = {}
                    add_level(new_dict, key)  # Chama a função recursivamente
                    check_n_update(key, data, new_dict)
                else:
                    check_n_update(key, data, value)

        add_level(self.data)
        self.save_data()
        print('Dados adicionados com sucesso!')

    def generate_pdf(self) -> None:
        pdf: FPDF = FPDF()
        pdf.add_page()

        # Coluna destaque
        # -------------------------------------------------------------------------------
        pdf.set_fill_color(189, 236, 182)  # Definindo a cor de destaque
        pdf.rect(0, 0, 55, 297, 'F')  # (A4: 210x297 mm)

        # Foto
        if os.path.exists(os.path.join('Images', 'foto.png')):
            pdf.image(os.path.join('Images', 'foto.png'), x=5, y=8, w=45)  # x, y e largura em mm

        largura_coluna: float = 55 - 2 * pdf.l_margin

        def add_contato(subcategory: str, use_link: bool = False):
            if subcategory in self.data['Contato']:
                if os.path.exists(os.path.join('Images', subcategory + '.png')):
                    pdf.image(os.path.join('Images', subcategory + '.png'), x=5, y=pdf.get_y() + 2.5, h=5)  # y centraliza com o texto
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
        pdf.set_font('Helvetica', size=10)
        pdf.multi_cell(140, 5, self.data['Resumo'])

        # Tecnologias
        if 'Tecnologias' in self.data:
            print(f'Selecione as tecnologias para incluir no currículo:')
            id_tec = {i + 1: item for i, item in enumerate(self.data['Tecnologias'])}
            for key, value in id_tec.items():
                print(f'{key}. {value}')
            selected_indices = input(f'Digite os números das tecnologias em ordem (separados por vírgula): ').split(
                ','
            )
            selected_indices = [int(index.strip()) for index in selected_indices if index.strip()]
            if selected_indices:
                pdf.set_font('Helvetica', size=12, style='B')
                pdf.set_y(pdf.get_y() + 5)
                pdf.set_x(60)
                pdf.cell(140, 5, 'Tecnologias', ln=True)
                pdf.set_font('Helvetica', size=12)
                pdf.set_x(60)
                tecnologies = ', '.join([id_tec[i] for i in selected_indices])
                pdf.multi_cell(140, 10, tecnologies)

        # Experiências
        if 'Experiências' in self.data:
            print(f'Selecione as experiências para incluir no currículo:')
            id_xp = {i + 1: item for i, item in enumerate(self.data['Experiências'])}
            for key, value in id_xp.items():
                print(f'{key}. {value}')
            selected_indices = input(f'Digite os números das experiências (separados por vírgula): ').split(',')
            selected_indices = [int(index.strip()) for index in selected_indices if index.strip()]
            if selected_indices:
                pdf.set_y(pdf.get_y() + 5)
                pdf.set_x(60)
                pdf.set_font('Helvetica', size=12, style='B')
                pdf.cell(140, 5, 'Experiências', ln=True)
                for index in selected_indices:
                    pdf.set_x(60)
                    pdf.set_font('Helvetica', size=12)
                    pdf.cell(140, 5, self.data['Experiências'][id_xp[index]]['Nome'], ln=True)
                    pdf.set_x(60)
                    pdf.set_font('Helvetica', size=12, style='I')
                    pdf.cell(
                        140,
                        5,
                        f'{self.data['Experiências'][id_xp[index]]['Período']} - {self.data['Experiências'][id_xp[index]]['Empresa']}',
                        ln=True,
                    )
                    pdf.set_x(60)
                    pdf.set_font('Helvetica', size=10)
                    pdf.multi_cell(140, 5, self.data['Experiências'][id_xp[index]]['Resumo'])
                    pdf.set_y(pdf.get_y() + 5)

        # Idiomas
        if 'Idiomas' in self.data:
            print('Selecione os Idiomas para incluir no currículo:')
            id_language = {i + 1: item for i, item in enumerate(self.data['Idiomas'])}
            for key, value in id_language.items():
                print(f'{key}. {value}')
            selected_indices = input('Digite os números dos idiomas (separados por vírgula): ').split(',')
            selected_indices = [int(index.strip()) for index in selected_indices if index.strip()]
            if selected_indices:
                pdf.set_font('Helvetica', size=12, style='B')
                pdf.set_y(pdf.get_y() + 5)
                pdf.set_x(60)
                pdf.cell(140, 5, 'Idiomas', ln=True)
                for index in selected_indices:
                    pdf.set_font('Helvetica', size=12)
                    pdf.set_x(60)
                    pdf.cell(140, 10, f'- {id_language[index]}', ln=True)

        # Cursos
        if 'Cursos' in self.data:
            print('Selecione os Cursos para incluir no currículo:')
            id_course = {i + 1: item for i, item in enumerate(self.data['Cursos'])}
            for key, value in id_course.items():
                print(f'{key}. {value}')
            selected_indices = input('Digite os números dos cursos (separados por vírgula): ').split(',')
            selected_indices = [int(index.strip()) for index in selected_indices if index.strip()]
            if selected_indices:
                pdf.set_font('Helvetica', size=12, style='B')
                pdf.set_y(pdf.get_y() + 5)
                pdf.set_x(60)
                pdf.cell(140, 5, 'Cursos', ln=True)
                for index in selected_indices:
                    pdf.set_font('Helvetica', size=12)
                    pdf.set_x(60)
                    pdf.cell(140, 5, id_course[index], ln=True)
                    pdf.set_font('Helvetica', size=12, style='I')
                    pdf.set_x(60)
                    pdf.cell(140, 10, self.data['Cursos'][id_course[index]], ln=True)
                    pdf.set_y(pdf.get_y() + 5)

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
                curriculum.add_data()
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
