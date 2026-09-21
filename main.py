import os
import shutil
import mimetypes

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.popup import Popup
from kivy.metrics import dp
from kivy.utils import platform


EXTENSOES = {
    ".pdf", ".doc", ".docx",
    ".htm", ".html",
    ".ppt", ".pptx",
    ".txt", ".epub",
}


def nome_legivel(nome):
    base = os.path.splitext(nome)[0]
    base = base.replace("_", " ").replace("-", " ")
    return " ".join(base.split())


def mime_do_arquivo(caminho):
    ext = os.path.splitext(caminho)[1].lower()

    tipos = {
        ".pdf": "application/pdf",
        ".doc": "application/msword",
        ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ".ppt": "application/vnd.ms-powerpoint",
        ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        ".txt": "text/plain",
        ".htm": "text/html",
        ".html": "text/html",
        ".epub": "application/epub+zip",
    }

    return tipos.get(ext) or mimetypes.guess_type(caminho)[0] or "*/*"


class ListaLivros(ScrollView):

    def __init__(self, pasta, **kwargs):
        super().__init__(**kwargs)

        self.pasta = pasta
        self.do_scroll_x = False

        self.lista = GridLayout(
            cols=1,
            spacing=dp(7),
            padding=[dp(10), dp(10)],
            size_hint_y=None,
        )

        self.lista.bind(
            minimum_height=self.lista.setter("height")
        )

        self.add_widget(self.lista)
        self.carregar()

    def carregar(self):
        self.lista.clear_widgets()

        if not os.path.isdir(self.pasta):
            aviso = Label(
                text="Pasta da biblioteca não encontrada.",
                size_hint_y=None,
                height=dp(70),
            )
            self.lista.add_widget(aviso)
            return

        arquivos = []

        for nome in os.listdir(self.pasta):
            caminho = os.path.join(self.pasta, nome)

            if not os.path.isfile(caminho):
                continue

            ext = os.path.splitext(nome)[1].lower()

            if ext in EXTENSOES:
                arquivos.append(nome)

        arquivos.sort(key=lambda x: x.casefold())

        if not arquivos:
            aviso = Label(
                text="Nenhum documento encontrado.",
                size_hint_y=None,
                height=dp(70),
            )
            self.lista.add_widget(aviso)
            return

        for nome in arquivos:
            caminho = os.path.join(self.pasta, nome)

            botao = Button(
                text=nome_legivel(nome),
                size_hint_y=None,
                height=dp(62),
                halign="left",
                valign="middle",
                padding=[dp(16), dp(8)],
            )

            botao.bind(
                size=lambda instance, value:
                setattr(instance, "text_size", (value[0] - dp(32), None))
            )

            botao.bind(
                on_release=lambda instance, arq=caminho:
                App.get_running_app().abrir_documento(arq)
            )

            self.lista.add_widget(botao)


class BibliotecaCasaisApp(App):

    title = "Biblioteca de Casais"

    def build(self):
        raiz = BoxLayout(
            orientation="vertical",
            spacing=dp(5),
        )

        titulo = Label(
            text="[b]BIBLIOTECA DE CASAIS[/b]",
            markup=True,
            size_hint_y=None,
            height=dp(65),
            font_size="22sp",
        )

        raiz.add_widget(titulo)

        abas = TabbedPanel(
            do_default_tab=False,
            tab_height=dp(52),
        )

        pasta_base = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "biblioteca",
        )

        pasta_principais = os.path.join(
            pasta_base,
            "principais",
        )

        pasta_complementar = os.path.join(
            pasta_base,
            "complementar",
        )

        aba_principais = TabbedPanelItem(
            text="PRINCIPAIS"
        )

        aba_principais.add_widget(
            ListaLivros(pasta_principais)
        )

        aba_complementar = TabbedPanelItem(
            text="COMPLEMENTARES"
        )

        aba_complementar.add_widget(
            ListaLivros(pasta_complementar)
        )

        abas.add_widget(aba_principais)
        abas.add_widget(aba_complementar)

        abas.default_tab = aba_principais
        abas.switch_to(aba_principais)

        raiz.add_widget(abas)

        return raiz

    def mensagem(self, titulo, texto):
        caixa = BoxLayout(
            orientation="vertical",
            padding=dp(15),
            spacing=dp(10),
        )

        mensagem = Label(
            text=texto,
            halign="center",
            valign="middle",
        )

        mensagem.bind(
            size=lambda instance, value:
            setattr(instance, "text_size", value)
        )

        fechar = Button(
            text="FECHAR",
            size_hint_y=None,
            height=dp(48),
        )

        caixa.add_widget(mensagem)
        caixa.add_widget(fechar)

        popup = Popup(
            title=titulo,
            content=caixa,
            size_hint=(0.88, 0.45),
        )

        fechar.bind(on_release=popup.dismiss)
        popup.open()

    def abrir_documento(self, origem):
        if not os.path.isfile(origem):
            self.mensagem(
                "Arquivo não encontrado",
                "O documento não foi localizado dentro da biblioteca.",
            )
            return

        if platform != "android":
            self.mensagem(
                "Documento selecionado",
                origem,
            )
            return

        try:
            self.abrir_android(origem)

        except Exception as erro:
            self.mensagem(
                "Erro ao abrir documento",
                str(erro),
            )

    def abrir_android(self, origem):
        from jnius import autoclass, cast

        PythonActivity = autoclass(
            "org.kivy.android.PythonActivity"
        )

        Intent = autoclass(
            "android.content.Intent"
        )

        FileProvider = autoclass(
            "androidx.core.content.FileProvider"
        )

        activity = PythonActivity.mActivity
        context = activity.getApplicationContext()

        pasta_saida = os.path.join(
            context.getCacheDir().getAbsolutePath(),
            "documentos",
        )

        os.makedirs(pasta_saida, exist_ok=True)

        destino = os.path.join(
            pasta_saida,
            os.path.basename(origem),
        )

        shutil.copy2(origem, destino)

        File = autoclass("java.io.File")
        arquivo_java = File(destino)

        autoridade = (
            context.getPackageName()
            + ".fileprovider"
        )

        uri = FileProvider.getUriForFile(
            context,
            autoridade,
            arquivo_java,
        )

        intent = Intent(Intent.ACTION_VIEW)

        intent.setDataAndType(
            uri,
            mime_do_arquivo(destino),
        )

        intent.addFlags(
            Intent.FLAG_GRANT_READ_URI_PERMISSION
        )

        intent.addFlags(
            Intent.FLAG_ACTIVITY_NEW_TASK
        )

        try:
            activity.startActivity(intent)

        except Exception:
            chooser = Intent.createChooser(
                intent,
                "Abrir documento com"
            )

            activity.startActivity(
                cast(
                    "android.content.Intent",
                    chooser
                )
            )


if __name__ == "__main__":
    BibliotecaCasaisApp().run()
