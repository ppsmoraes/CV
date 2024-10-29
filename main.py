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
                self.data[category] = list()
            self.data[category].append(data)
        else:
            if category not in self.data:
                self.data[category] = dict()
            if subcategory not in self.data[category]:
                self.data[category][subcategory] = list()
            self.data[category][subcategory].append(data)
        self.save_data()

    def generate_pdf(self):
        pdf = FPDF()
        pdf.add_page()

        pdf.set_fill_color(189, 236, 182)  # Definindo a cor de destaque
        pdf.rect(0, 0, 55, 297, 'F')  # (A4: 210x297 mm)

        # Foto
        try:
            pdf.image(r'Images\foto.png', x=5, y=8, w=45)  # x, y e largura em mm
        except Exception as e:
            print(f'Erro ao adicionar a imagem: {e}')

        # Nome
        pdf.set_x(60)  # Move para a direita
        pdf.set_font('Helvetica', size=16, style='B')
        pdf.cell(140, 5, self.data.get('Nome', ['Fulano da Silva'])[0], ln=True)

        # Vaga
        pdf.set_x(60)  # Move para a direita
        pdf.set_font('Helvetica', size=14)
        pdf.cell(140, 10, self.data.get('Vaga', ['Nome da Vaga'])[0], ln=True)

        # Resumo
        pdf.set_x(60)  # Move para a direita
        pdf.set_font('Helvetica', size=12)
        pdf.multi_cell(
            140,
            5,
            'Esse é um resumo. Aqui você deve deixar uma mensagem personalizada para cada currículo gerado baseado na vaga a qual esse currículo será aplicado.',
        )

        # TODO aqui deve ir as tecnologias
        
        largura_coluna = 55-2*pdf.l_margin
        pdf.set_y(60) # Move para baixo da foto
        pdf.set_font('Helvetica', size=12, style='B')
        pdf.cell(largura_coluna, 10, 'Contato', ln=True, align='C')

        pdf.set_font('Helvetica', size=10, style='U')
        pdf.set_text_color(1, 75, 160)  # Azul
        pdf.image(r'Images\Github.png', x=5, y=pdf.get_y()+2.5, h=5) # Centraliza com o texto
        pdf.cell(largura_coluna, 10, self.data['Contato'].get('Github')[0], ln=True, link=f'https://{self.data['Contato'].get('Github')[0]}')

        pdf.image(r'Images\Linkedin.png', x=5, y=pdf.get_y()+2.5, h=5)
        pdf.cell(largura_coluna, 10, self.data['Contato'].get('Linkedin')[0], ln=True, link=f'https://{self.data['Contato'].get('Linkedin')[0]}')

        pdf.set_font('Helvetica', size=10)
        pdf.set_text_color(0, 0, 0)  # Preto
        pdf.image(r'Images\Email.png', x=5, y=pdf.get_y()+2.5, h=5)
        pdf.cell(largura_coluna, 10, self.data['Contato'].get('E-mail')[0], ln=True)

        pdf.image(r'Images\Whatsapp.png', x=5, y=pdf.get_y()+2.5, h=5)
        pdf.cell(largura_coluna, 10, self.data['Contato'].get('Telefone')[0], ln=True)
        
        # TODO Remover duplicatas

        # Selecionar experiências
        if 'experiencia' in self.data:
            print('Selecione as experiências para incluir no currículo:')
            for i, exp in enumerate(self.data['experiencia']):
                print(f'{i + 1}. {exp}')
            selected_indices = input('Digite os números das experiências (separados por vírgula): ').split(',')
            selected_indices = [index.strip() for index in selected_indices if index.strip()]
            if selected_indices:
                pdf.cell(200, 10, ln=True)  # Linha em branco
                pdf.set_font('Helvetica', size=12, style='B')
                pdf.cell(200, 10, 'Experiências', ln=True)
                pdf.set_font('Helvetica', size=12)
                for index in selected_indices:
                    if index.strip().isdigit() and 0 < int(index) <= len(self.data['experiencia']):
                        pdf.cell(200, 10, f'- {self.data['experiencia'][int(index) - 1]}', ln=True)

        # Selecionar cursos
        if 'cursos' in self.data:
            print('Selecione os cursos para incluir no currículo:')
            for i, course in enumerate(self.data['cursos']):
                print(f'{i + 1}. {course}')
            selected_indices = input('Digite os números dos cursos (separados por vírgula): ').split(',')
            selected_indices = [index.strip() for index in selected_indices if index.strip()]
            if selected_indices:
                pdf.cell(200, 10, ln=True)  # Linha em branco
                pdf.set_font('Helvetica', size=12, style='B')
                pdf.cell(200, 10, 'Cursos', ln=True)
                pdf.set_font('Helvetica', size=12)
                for index in selected_indices:
                    if index.strip().isdigit() and 0 < int(index) <= len(self.data['cursos']):
                        pdf.cell(200, 10, f'- {self.data['cursos'][int(index) - 1]}', ln=True)

        # Selecionar idiomas
        if 'idiomas' in self.data:
            print('Selecione os idiomas para incluir no currículo:')
            for i, lang in enumerate(self.data['idiomas']):
                print(f'{i + 1}. {lang}')
            selected_indices = input('Digite os números dos idiomas (separados por vírgula): ').split(',')
            selected_indices = [index.strip() for index in selected_indices if index.strip()]
            if selected_indices:
                pdf.cell(200, 10, ln=True)  # Linha em branco
                pdf.set_font('Helvetica', size=12, style='B')
                pdf.cell(200, 10, 'Idiomas', ln=True)
                pdf.set_font('Helvetica', size=12)
                for index in selected_indices:
                    if index.strip().isdigit() and 0 < int(index) <= len(self.data['idiomas']):
                        pdf.cell(200, 10, f'- {self.data['idiomas'][int(index) - 1]}', ln=True)

        # Selecionar habilidades
        if 'habilidades' in self.data:
            print('Selecione as habilidades para incluir no currículo:')
            for i, skill in enumerate(self.data['habilidades']):
                print(f'{i + 1}. {skill}')
            selected_indices = input('Digite os números das habilidades (separados por vírgula): ').split(',')
            selected_indices = [index.strip() for index in selected_indices if index.strip()]
            if selected_indices:
                pdf.cell(200, 10, ln=True)  # Linha em branco
                pdf.set_font('Helvetica', size=12, style='B')
                pdf.cell(200, 10, 'Habilidades', ln=True)
                pdf.set_font('Helvetica', size=12)
                for index in selected_indices:
                    if index.strip().isdigit() and 0 < int(index) <= len(self.data['habilidades']):
                        pdf.cell(200, 10, f'- {self.data['habilidades'][int(index) - 1]}', ln=True)

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
                            print(f'\nSubmenu "Adicionar {category}":')
                            if category in curriculum.data:
                                print(f'Subcategorias: {[key for key in curriculum.data[category].keys()]}')
                            print('Digite "back" para voltar para o menu principal')
                            print('Pressione enter para seguir sem subcategoria')
                            
                            subcategory = input('Escolha uma subcategoria: ')

                            match subcategory.strip():
                                case '':
                                    data = input(f'Digite seu(a) {category}: ')
                                    curriculum.add_data(category, data)
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
