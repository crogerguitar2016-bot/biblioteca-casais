import os
import subprocess

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView


# Pastas que não devem ser percorridas
PASTAS_IGNORADAS = {
    "/storage/emulated/0/Android/data",
    "/storage/emulated/0/Android/obb",
}


# Termos relacionados a casamento e vida conjugal
TERMOS = [
    "casal",
    "casais",
    "casamento",
    "casamentos",
    "matrimonio",
    "matrimônio",
    "conjugal",
    "conjuge",
    "cônjuge",
    "relacionamento",
    "relacionamentos",
    "marido",
    "esposa",
    "esposo",
    "namoro",
    "namorados",
    "noivo",
    "noiva",
    "noivos",
    "fidelidade",
    "aconselhamento",
]


EXTENSOES = {
    ".pdf",
    ".doc",
    ".docx",
    ".txt",
    ".html",
    ".htm",
    ".ppt",
    ".pptx",
}


def arquivo_relevante(nome):
    nome_minusculo = nome.lower()
    return any(termo in nome_minusculo for termo in TERMOS)


def abrir_arquivo(caminho):
    """
    Tenta abrir o documento usando o aplicativo Android associado.
    """
    try:
        subprocess.Popen([
            "am",
            "start",
            "-a",
            "android.intent.action.VIEW",
            "-d",
            "file://" + caminho,
        ])
    except Exception as erro:
        print("Erro ao abrir:", erro)


class BibliotecaCasais(App):

    def build(self):
        self.title = "Biblioteca de Casais"

        raiz = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=8
        )

        titulo = Label(
            text="BIBLIOTECA DE CASAIS",
            size_hint_y=None,
            height=50,
            font_size=22
        )

        raiz.add_widget(titulo)

        self.pesquisa = TextInput(
            hint_text="Pesquisar documento...",
            size_hint_y=None,
            height=48,
            multiline=False
        )

        raiz.add_widget(self.pesquisa)

        botao_buscar = Button(
            text="🔎 BUSCAR DOCUMENTOS",
            size_hint_y=None,
            height=50
        )

        botao_buscar.bind(on_press=self.buscar)

        raiz.add_widget(botao_buscar)

        self.status = Label(
            text="Toque em BUSCAR para procurar documentos.",
            size_hint_y=None,
            height=45
        )

        raiz.add_widget(self.status)

        scroll = ScrollView()

        self.lista = BoxLayout(
            orientation="vertical",
            spacing=5,
            size_hint_y=None
        )

        self.lista.bind(
            minimum_height=self.lista.setter("height")
        )

        scroll.add_widget(self.lista)

        raiz.add_widget(scroll)

        return raiz

    def buscar(self, *args):
        self.lista.clear_widgets()

        termo_pesquisa = self.pesquisa.text.lower().strip()

        encontrados = []

        base = "/storage/emulated/0"

        for raiz, diretorios, arquivos in os.walk(base):

            # Não entrar em Android/data e Android/obb
            diretorios[:] = [
                d for d in diretorios
                if os.path.join(raiz, d) not in PASTAS_IGNORADAS
            ]

            for nome in arquivos:

                extensao = os.path.splitext(nome)[1].lower()

                if extensao not in EXTENSOES:
                    continue

                if not arquivo_relevante(nome):
                    continue

                if termo_pesquisa and termo_pesquisa not in nome.lower():
                    continue

                caminho = os.path.join(raiz, nome)

                encontrados.append(caminho)

        encontrados.sort(key=lambda x: x.lower())

        self.status.text = (
            f"{len(encontrados)} documento(s) encontrado(s)."
        )

        if not encontrados:
            self.lista.add_widget(
                Label(
                    text="Nenhum documento encontrado.",
                    size_hint_y=None,
                    height=50
                )
            )
            return

        for caminho in encontrados:

            nome = os.path.basename(caminho)

            botao = Button(
                text=nome,
                size_hint_y=None,
                height=55
            )

            botao.bind(
                on_press=lambda instance, c=caminho:
                abrir_arquivo(c)
            )

            self.lista.add_widget(botao)


if __name__ == "__main__":
    BibliotecaCasais().run()
