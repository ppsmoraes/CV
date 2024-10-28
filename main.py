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
        return {'dados_pessoais': {}, 'experiencia': [], 'cursos': [], 'idiomas': [], 'habilidades': []}

    def set_dados_pessoais(self, nome, telefone, email):
        self.data['dados_pessoais'] = {'nome': nome, 'telefone': telefone, 'email': email}
        self.save_data()

    def save_data(self):
        with open(self.filename, 'w') as file:
            json.dump(self.data, file)

    def add_experience(self, experience):
        self.data['experiencia'].append(experience)
        self.save_data()

    def add_course(self, course):
        self.data['cursos'].append(course)
        self.save_data()

    def add_language(self, language):
        self.data['idiomas'].append(language)
        self.save_data()

    def add_skill(self, skill):
        self.data['habilidades'].append(skill)
        self.save_data()

    def generate_pdf(self):
        pdf = FPDF()
        pdf.add_page()

        pdf.set_fill_color(230, 230, 250)  # Definindo a cor de destaque
        pdf.rect(0, 0, 50, 297, 'F')  # (A4: 210x297 mm)

        # Adiciona a foto
        try:
            pdf.image(r'Image\PostgreSQL.png', x=10, y=8, w=33)  # x, y e largura em mm
        except Exception as e:
            print(f"Erro ao adicionar a imagem: {e}")

        pdf.set_font("Arial", size=12)

        # Adiciona os dados pessoais
        pdf.set_x(55)  # Move para a direita
        pdf.cell(200, 10, txt=f"Nome: {self.data['dados_pessoais'].get('nome', 'N/A')}", ln=True)
        pdf.set_x(55)  # Move para a direita
        pdf.cell(200, 10, txt=f"Telefone: {self.data['dados_pessoais'].get('telefone', 'N/A')}", ln=True)
        pdf.set_x(55)  # Move para a direita
        pdf.cell(200, 10, txt=f"E-mail: {self.data['dados_pessoais'].get('email', 'N/A')}", ln=True)
        pdf.cell(200, 10, ln=True)  # Linha em branco

        # Selecionar experiências
        if self.data['experiencia']:
            print("Selecione as experiências para incluir no currículo:")
            for i, exp in enumerate(self.data['experiencia']):
                print(f"{i + 1}. {exp}")
            selected_indices = input("Digite os números das experiências (separados por vírgula): ").split(',')
            selected_indices = [index.strip() for index in selected_indices if index.strip()]
            if selected_indices:
                pdf.cell(200, 10, ln=True)  # Linha em branco
                pdf.cell(200, 10, txt="Experiências:", ln=True)
                for index in selected_indices:
                    if index.strip().isdigit() and 0 < int(index) <= len(self.data['experiencia']):
                        pdf.cell(200, 10, txt=f"- {self.data['experiencia'][int(index) - 1]}", ln=True)

        # Selecionar cursos
        if self.data['cursos']:
            print("Selecione os cursos para incluir no currículo:")
            for i, course in enumerate(self.data['cursos']):
                print(f"{i + 1}. {course}")
            selected_indices = input("Digite os números dos cursos (separados por vírgula): ").split(',')
            selected_indices = [index.strip() for index in selected_indices if index.strip()]
            if selected_indices:
                pdf.cell(200, 10, ln=True)  # Linha em branco
                pdf.cell(200, 10, txt="Cursos:", ln=True)
                for index in selected_indices:
                    if index.strip().isdigit() and 0 < int(index) <= len(self.data['cursos']):
                        pdf.cell(200, 10, txt=f"- {self.data['cursos'][int(index) - 1]}", ln=True)

        # Selecionar idiomas
        if self.data['idiomas']:
            print("Selecione os idiomas para incluir no currículo:")
            for i, lang in enumerate(self.data['idiomas']):
                print(f"{i + 1}. {lang}")
            selected_indices = input("Digite os números dos idiomas (separados por vírgula): ").split(',')
            selected_indices = [index.strip() for index in selected_indices if index.strip()]
            if selected_indices:
                pdf.cell(200, 10, ln=True)  # Linha em branco
                pdf.cell(200, 10, txt="Idiomas:", ln=True)
                for index in selected_indices:
                    if index.strip().isdigit() and 0 < int(index) <= len(self.data['idiomas']):
                        pdf.cell(200, 10, txt=f"- {self.data['idiomas'][int(index) - 1]}", ln=True)

        # Selecionar habilidades
        if self.data['habilidades']:
            print("Selecione as habilidades para incluir no currículo:")
            for i, skill in enumerate(self.data['habilidades']):
                print(f"{i + 1}. {skill}")
            selected_indices = input("Digite os números das habilidades (separados por vírgula): ").split(',')
            selected_indices = [index.strip() for index in selected_indices if index.strip()]
            if selected_indices:
                pdf.cell(200, 10, ln=True)  # Linha em branco
                pdf.cell(200, 10, txt="Habilidades:", ln=True)
                for index in selected_indices:
                    if index.strip().isdigit() and 0 < int(index) <= len(self.data['habilidades']):
                        pdf.cell(200, 10, txt=f"- {self.data['habilidades'][int(index) - 1]}", ln=True)

        pdf.output("curriculo.pdf")
        print("PDF gerado com sucesso!")


def main():
    curriculum = Curriculum()

    while True:
        print("\nMenu:")
        print("1. Adicionar Dados Pessoais")
        print("2. Adicionar Experiência")
        print("3. Adicionar Curso")
        print("4. Adicionar Idioma")
        print("5. Adicionar Habilidade")
        print("6. Gerar PDF")
        print("7. Sair")

        choice = input("Escolha uma opção: ")

        match choice:
            case '1':
                nome = input("Digite seu nome: ")
                telefone = input("Digite seu telefone: ")
                email = input("Digite seu e-mail: ")
                curriculum.set_dados_pessoais(nome, telefone, email)
            case '2':
                experience = input("Digite a experiência de trabalho: ")
                curriculum.add_experience(experience)
            case '3':
                course = input("Digite o nome do curso: ")
                curriculum.add_course(course)
            case '4':
                language = input("Digite o idioma: ")
                curriculum.add_language(language)
            case '5':
                skill = input("Digite a habilidade: ")
                curriculum.add_skill(skill)
            case '6':
                curriculum.generate_pdf()
                print("Saindo...")
                break
            case '7':
                print("Saindo...")
                break
            case _:
                print("Opção inválida! Tente novamente.")


if __name__ == "__main__":
    main()
