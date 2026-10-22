"""FireRed IA: janela do painel (time com sprites oficiais, plano, mochila, capturas, histórico) com botões Jogar e Parar."""

import webview

from fireredia.painel import painel


def main():
    painel.iniciar()  # porta em uso: a IA já está servindo a mesma memória
    webview.create_window(
        "FireRed IA",
        f"http://127.0.0.1:{painel.PORTA}",
        width=1500,
        height=960,
        min_size=(900, 600),
        background_color="#0d0f13",
    )
    webview.start()


if __name__ == "__main__":
    main()
