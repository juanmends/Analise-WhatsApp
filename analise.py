import emoji
import pandas as pd
import re
import regex
from collections import Counter
import plotly.express as px

def startsWithDateAndTime(s):  # RETORNA TRUE CASO A MENSAGEM INICIE COM DATA E HORÁRIO
    pattern = r'^(\d{1,2}/\d{1,2}/\d{2,4}) (\d{1,2}:\d{2})(?: ?(AM|PM|am|pm))? -'
    result = re.match(pattern, s)
    return result


def encontraAutor(s):  # VERIFICA SE A STRING COMEÇA COM NOME DE UM AUTOR
    regex = r'^(.+?):'
    match = re.match(regex, s)
    return match


def getDataPoint(line):  # SEPARA AS INFORMAÇÕES DE UMA LINHA
    splitLine = line.split(' - ')
    dateTime = splitLine[0]
    date, time = dateTime.split(' ')
    message = splitLine[1]
    if encontraAutor(message):
        splitMessage = message.split(': ')
        author = splitMessage[0]
        message = ' '.join(splitMessage[1:])
    else:
        author = None
    return date, time, author, message


def split_count(text):
    emoji_list = []
    data = regex.findall(r'\X', text)
    for word in data:
        if any(emoji.is_emoji(char) for char in word):
            emoji_list.append(word)
    return emoji_list


def retorna_dia(i):
    dias = ["Segunda-Feira", "Terça-Feira", "Quarta-Feira", "Quinta-Feira", "Sexta-Feira", "Sábado", "Domingo"]
    return dias[i]


def analisar_conversa(filepath):
    # MAIN:

    ##MANIPULAÇÃO DO ARQUIVO
    parsedData = []

    with open(filepath, encoding="utf-8") as fp:
        fp.readline()  # PULANDO PRIMEIRA LINHA
        messageBuffer = []
        date, time, author = None, None, None
        while True:
            line = fp.readline()
            if not line:
                break
            line = line.strip()
            if startsWithDateAndTime(line):
                if len(messageBuffer) > 0:
                    parsedData.append([date, time, author, ' '.join(messageBuffer)])
                messageBuffer.clear()
                date, time, author, message = getDataPoint(line)
                messageBuffer.append(message)
            else:
                messageBuffer.append(line)

    ##MANIPULAÇÃO DO DATAFRAME
    df = pd.DataFrame(parsedData, columns=['date', 'time', 'author', 'message'])  # CRIA O DATAFRAME
    df['date'] = pd.to_datetime(df['date'], dayfirst=True)  # CONVERTE O VALOR DA DATA

    df = df.dropna()  # REMOVE TODAS AS LINHAS QUE CONTEM AO MENOS UM ELEMENTO NULO

    # EMOJIS
    df["emoji"] = df["message"].apply(split_count)

    todos_emojis = df["emoji"].tolist()
    lista_emojis = []

    for sublista in todos_emojis:
        for emoji in sublista:
            lista_emojis.append(emoji)

    contador = Counter(lista_emojis)

    mais_usados = contador.most_common(10)

    # SEPARANDO MÍDIA DE MENSAGENS
    media_messages_df = df[df["message"] == '<Mídia oculta>']
    messages_df = df.drop(media_messages_df.index)

    # CRIANDO COLUNAS DE LETRAS E PALAVRAS E CONTADOR DE MESAGENS
    messages_df["letters"] = messages_df["message"].apply(lambda s: len(s.replace(' ', '')))
    messages_df["wordsCount"] = messages_df["message"].apply(lambda s: len(s.split(' ')))
    messages_df["words"] = messages_df["message"].apply(lambda s: s.split(' '))
    messages_df["emojiCount"] = messages_df["emoji"].apply(lambda s: len(s))
    messages_df["messageCount"] = 1

    # DIAS
    day_df = pd.DataFrame(messages_df["message"])
    day_df["diaDaSemana"] = messages_df["date"].dt.weekday
    day_df["diaDaSemana"] = day_df["diaDaSemana"].apply(retorna_dia)
    day_df["messageCount"] = 1
    day = day_df.groupby("diaDaSemana").sum()
    day.reset_index(inplace=True)

    # DATAS
    date_df = messages_df.groupby("date").sum()
    date_df.reset_index(inplace=True)

    # STATUS DE CADA UM DOS AUTORES
    autores = messages_df["author"].unique()
    cards_html = ""
    for i in range(len(autores)):
        df_this = messages_df[messages_df["author"] == autores[i]]
        total_msgs = df_this.shape[0]
        palavras_por_msg = round((sum(df_this["wordsCount"]) / df_this.shape[0]), 2)
        media_count = media_messages_df[media_messages_df["author"] == autores[i]].shape[0]
        emojis_count = sum(df_this["emoji"].apply(lambda s: len(s)))
        # print("-"*35)
        # print(f'Dados - {autores[i]}')
        # print(f'Número de mensagens: {df_this.shape[0]}')
        # print(f'Palavras por mensagem: {round((sum(df_this["wordsCount"])/df_this.shape[0]),2)}')
        # print(f'Mídias enviadas: {media_messages_df[media_messages_df["author"] == autores[i]].shape[0]}')
        # print(f'Emojis enviados: {sum(df_this["emoji"].apply(lambda s : len(s)))}')
        todas_palavras = df_this['words'].tolist()
        lista_palavras = []
        for sublista in todas_palavras:
            for palavra in sublista:
                lista_palavras.append(palavra)
        lista_palavras_filtrada = []
        for palavra in lista_palavras:
            if len(palavra) > 4:
                lista_palavras_filtrada.append(palavra)
        palavras_mais = Counter(lista_palavras_filtrada).most_common(10)
        palavras_formatadas = ', '.join([f"{p} ({c})" for p, c in palavras_mais])
        # print(f'Palavras mais falada: {palavras_mais}')
        cards_html += f'''
            <div class="autor-card" onclick="this.classList.toggle('ativo')">
                <h3>👤 {autores[i]}</h3>
                <div class="autor-info">
                  <p><strong>Mensagens:</strong> {total_msgs}</p>
                  <p><strong>Palavras por mensagem:</strong> {palavras_por_msg}</p>
                  <p><strong>Mídias enviadas:</strong> {media_count}</p>
                  <p><strong>Emojis enviados:</strong> {emojis_count}</p>
                  <p><strong>Top palavras:</strong> {palavras_formatadas}</p>
                </div>
            </div>
            '''

    # INTERAÇÃO COM USUÁRIO
    # print('-'*35)
    # print(f'TOTAL DE MENSAGENS: {df.shape[0]}')
    # print(f'QUANTIDADE DE MÍDIAS ENVIADAS: {df[df['message']=='<Mídia oculta>'].shape[0]}')
    # print(f'QUANTIDADE MENSAGENS DE TEXTO: {df[~(df['message']=='<Mídia oculta>')].shape[0]}')
    # print(f'EMOJIS MAIS USADOS: {mais_usados}')
    df_emoji = pd.DataFrame(contador.items(), columns=['emoji', 'count'])
    fig_emoji = px.pie(df_emoji, values='count', names='emoji')
    fig_emoji.update_traces(textposition='inside', textinfo='percent+label')
    fig_emoji.write_html("static/graficos/emoji.html")
    # fig_emoji.show()
    fig_dias = px.line_polar(day, r='messageCount', theta='diaDaSemana', line_close=True)
    fig_dias.update_traces(fill='toself')
    fig_dias.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
            )),
        showlegend=False
    )
    fig_dias.write_html("static/graficos/dias.html")
    # fig_dias.show()
    fig_datas = px.line(date_df, x='date', y='messageCount')
    fig_datas.update_xaxes(nticks=20)
    fig_datas.write_html("static/graficos/datas.html")
    # fig_datas.show()

    # HTML
    f = open("templates/index.html", "w", encoding="utf-8")
    html_template = f'''<!DOCTYPE html>
    <html lang="pt-BR">
    <head>
      <meta charset="UTF-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <title>Análise WhatsApp</title>
      <link
        rel="icon"
        type="image/png"
        href="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg"
      />
      <link
        href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap"
        rel="stylesheet"
      />
      <style>
        body {{
          background: linear-gradient(135deg, #e0f7fa, #f0f4f8);
          color: #333;
          font-family: "Roboto", sans-serif;
          margin: 0;
          padding: 0;
          display: flex;
          flex-direction: column;
          min-height: 100vh;
        }}

        header {{
          background-color: #00b894;
          color: white;
          padding: 30px 0;
          text-align: center;
          box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }}

        header h1 {{
          margin: 0;
          font-size: 2.5em;
          letter-spacing: 1px;
        }}

        nav {{
          background: #ffffffdd;
          display: flex;
          justify-content: center;
          gap: 40px;
          padding: 12px 30px;
          margin: 20px auto;
          max-width: 600px;
          border-radius: 40px;
          box-shadow: 0 8px 20px rgba(0, 184, 148, 0.15);
          backdrop-filter: saturate(180%) blur(10px);
          -webkit-backdrop-filter: saturate(180%) blur(10px);
          transition: box-shadow 0.3s ease;
        }}

        nav:hover {{
          box-shadow: 0 12px 30px rgba(0, 184, 148, 0.3);
        }}

        nav a {{
          color: #00b894;
          text-decoration: none;
          font-weight: 700;
          font-size: 1.2em;
          padding: 8px 18px;
          border-radius: 30px;
          transition: background-color 0.3s, color 0.3s, transform 0.2s;
          user-select: none;
        }}

        nav a:hover,
        nav a:focus {{
          background-color: #00b894;
          color: white;
          transform: translateY(-3px);
          outline: none;
          box-shadow: 0 5px 15px rgba(0, 184, 148, 0.4);
          cursor: pointer;
        }}

        main {{
          max-width: 1000px;
          margin: 40px auto;
          padding: 40px;
          background-color: #ffffff;
          border-radius: 16px;
          box-shadow: 0 12px 24px rgba(0, 0, 0, 0.08);
          flex-grow: 1;
        }}

        h2 {{
          color: #2d3436;
          font-size: 1.8em;
          border-bottom: 2px solid #00b894;
          padding-bottom: 10px;
          margin-bottom: 25px;
        }}

        .info-geral p {{
          font-size: 1.8em;
          margin-bottom: 20px;
          color: #2d3436;
        }}

        .info-geral p span {{
          font-weight: bold;
          color: #00b894;
        }}

        .autores {{
          display: flex;
          flex-direction: column;
          gap: 20px;
        }}

        .autor-card {{
          background-color: #f1f8e9;
          border: 2px solid #00b894;
          border-radius: 12px;
          padding: 15px 20px;
          cursor: pointer;
          transition: all 0.3s ease;
          box-shadow: 0 4px 10px rgba(0, 184, 148, 0.2);
        }}

        .autor-card h3 {{
          margin: 0;
          font-size: 1.4em;
          color: #00b894;
        }}

        .autor-info {{
          max-height: 0;
          overflow: hidden;
          transition: max-height 0.3s ease;
        }}

        .autor-card.ativo .autor-info {{
          max-height: 500px; /* Ajuste conforme necessário */
          margin-top: 10px;
        }}

        .autor-info p {{
          margin: 5px 0;
        }}

        footer {{
          background-color: #2d3436;
          color: #dfe6e9;
          text-align: center;
          padding: 15px 10px;
          font-size: 0.95em;
          margin-top: auto;
        }}

        footer p {{
          margin: 5px 0;
        }}

        @media (max-width: 700px) {{
          nav {{
            max-width: 90%;
            gap: 25px;
            padding: 12px 20px;
          }}

          nav a {{
            font-size: 1em;
            padding: 6px 12px;
          }}

          main {{
            margin: 20px 10px;
            padding: 20px;
          }}
        }}

      </style>
    </head>
    <body>
      <header>
        <h1>Análise de Mensagens WhatsApp</h1>
      </header>

      <nav>
        <a href="emoji">📊 Emojis</a>
        <a href="dias">📅 Dias da Semana</a>
        <a href="datas">📈 Datas</a>
      </nav>

      <main>
        <h2>Informações Gerais</h2>
        <div class="info-geral">
          <p>Total de mensagens: <span>{df.shape[0]}</span></p>
          <p>Quantidade de mídias enviadas: <span>{df[df['message'] == '<Mídia oculta>'].shape[0]}</span></p>
          <p>Quantidade de mensagens de texto: <span>{df[~(df['message'] == '<Mídia oculta>')].shape[0]}</span></p>
        </div>
        <h2>Estatísticas por Participante</h2>
      <div class="autores">
        {cards_html}
      </div>
      </main>

      <footer>
        <p>Desenvolvido por Juan Silva Mendes</p>
        <p>Projeto feito com Python 🐍</p>
      </footer>
    </body>
    </html>'''
    f.write(html_template)
    f.close()