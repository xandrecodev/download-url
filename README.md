# DownloadUrl

Aplicativo desktop em Python para baixar imagens a partir de URLs informadas pelo usuário.

## O que ele faz

O programa abre uma interface gráfica com Tkinter, permite colar vários links de imagens separados por ponto e vírgula (`;`), escolhe a pasta de destino e inicia o download automaticamente.

Ele valida:

- se os links são válidos (`http://` ou `https://`)
- se o servidor responde com conteúdo de imagem
- se a resposta não está vazia
- se a pasta de destino existe ou pode ser criada

## Requisitos

- Python 3.8+
- Biblioteca padrão do Python (`tkinter`, `urllib`, `mimetypes`, `os`, `threading`)

A maioria dos sistemas com Python já instala o `tkinter` junto com o interpretador.

## Como executar

No diretório do projeto, rode:

```bash
python download.py
```

## Como usar

1. Copie os links das imagens que deseja baixar.
2. Separe cada URL por ponto e vírgula (`;`).
3. Cole os links na caixa de texto.
4. Clique em `Escolher pasta...` para definir onde as imagens serão salvas.
5. Clique em `Baixar imagens`.
6. Acompanhe o progresso no painel de log.

Exemplo:

```text
https://exemplo.com/imagem1.jpg; https://exemplo.com/imagem2.png; https://exemplo.com/imagem3.webp
```

## Observações

- O programa salva as imagens na pasta `imagens_baixadas` dentro do diretório do projeto por padrão.
- Só são aceitas URLs que retornem um `Content-Type` do tipo imagem, como `image/jpeg`, `image/png` e `image/webp`.
- Caso algum link falhe, o programa registra a falha no log e continua com os demais.

## Estrutura do projeto

```text
DownloadUrl/
├── download.py
├── README.md
└── imagens_baixadas/
```

A pasta `imagens_baixadas` é criada automaticamente quando o download começa.

## Licença

Este projeto foi desenvolvido para uso local e pessoal. Ajustes podem ser feitos conforme a necessidade do usuário.
