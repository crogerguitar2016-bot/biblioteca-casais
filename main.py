main.py     "Nenhum documento "
                        "encontrado."
                    ),
                    size_hint_y=None,
                    height=dp(50),
                    font_size="16sp",
                )
            )

            return

        if mostrar_categorias:

            if self.principais:

                self.adicionar_titulo_secao(
                    "BIBLIOTECA PRINCIPAL "
                    f"({len(self.principais)})"
                )

                documentos_principais = [
                    documento
                    for documento in self.documentos
                    if documento["categoria"]
                    == "principal"
                ]

                for documento in (
                    documentos_principais
                ):

                    self.adicionar_documento(
                        documento
                    )

            if self.complementares:

                self.adicionar_titulo_secao(
                    "MATERIAIS COMPLEMENTARES "
                    f"({len(self.complementares)})"
                )

                documentos_complementares = [
                    documento
                    for documento in self.documentos
                    if documento["categoria"]
                    == "complementar"
                ]

                for documento in (
                    documentos_complementares
                ):

                    self.adicionar_documento(
                        documento
                    )

        else:

            for documento in documentos:

                self.adicionar_documento(
                    documento
                )

    def filtrar(
        self,
        instance,
        texto
    ):

        termo = texto.strip().lower()

        if not termo:

            self.status.text = (
                "Biblioteca interna: "
                f"{len(self.documentos)} "
                "documento(s)"
            )

            self.mostrar_documentos(
                self.documentos,
                mostrar_categorias=True
            )

            return

        encontrados = [
            documento
            for documento
            in self.documentos
            if (
                termo
                in documento["nome"].lower()
                or termo
                in documento["arquivo"].lower()
            )
        ]

        self.status.text = (
            f"{len(encontrados)} "
            "documento(s) encontrado(s)"
        )

        self.mostrar_documentos(
            encontrados,
            mostrar_categorias=False
        )

    def mostrar_mensagem(
        self,
        mensagem
    ):

        self.lista.clear_widgets()

        self.lista.add_widget(
            Label(
                text=mensagem,
                size_hint_y=None,
                height=dp(80),
                font_size="16sp",
            )
        )


if __name__ == "__main__":

    BibliotecaCasais().run()
