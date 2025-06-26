# 📊 Analise-WhatsApp

## Sobre o projeto

**Analise-WhatsApp** é uma ferramenta web desenvolvida em **Python** com **Flask**, que permite analisar o conteúdo de um chat exportado do WhatsApp Android (.txt) de forma visual e interativa. O usuário pode fazer upload do arquivo, gerar estatísticas e visualizar gráficos sobre emojis, frequência de mensagens por dias da semana e ao longo do tempo.

Baseado nos projetos:

- https://matheusrdsantos.medium.com/analizando-dados-de-grupos-de-whatsapp-com-python-6fa90ed493b4
- https://github.com/kurasaiteja/Whatsapp-Analysis/blob/master/Whatsapp_Group_Chat_Analysis_for_Android.ipynb

---

## 🚀 Tecnologias utilizadas

O projeto utiliza uma combinação de tecnologias que destacam:

- **Python** — análise e processamento de dados
- **Flask** — criação de servidor web leve e responsivo
- **Pandas** — manipulação de dados estruturados
- **Plotly** — visualização interativa de gráficos
- **HTML5 + CSS3** — front-end moderno e responsivo
- **Regex** — extração de informações de texto com expressões regulares
- **Git + GitHub** — controle de versão e colaboração

---

## 💡 Funcionalidades

- ✅ Upload de arquivos de conversas `.txt` exportados do WhatsApp
- ✅ Detecção de autores, palavras, emojis e mídias
- ✅ Geração de gráficos interativos:
  - **📊 Emojis mais usados**
  - **📅 Dias da semana mais ativos**
  - **📈 Frequência ao longo do tempo**
- ✅ Estatísticas individuais por participante
- ✅ Interface web amigável e fácil de usar

---

## 📷 Demonstrações

### 🔻 Página de upload
![Página de upload](/exemplos/1.png)

### 🔻 Análise Geral
![Análise Geral](/exemplos/2.png)

### 🔻 Análise por participante
![Análise por participante](/exemplos/3.png)

### 🔻 Emojis mais usados
![Gráfico de emojis](/exemplos/4.png)

### 🔻 Atividade por dia da semana
![Gráfico dias da semana](/exemplos/5.png)

### 🔻 Evolução temporal das mensagens
![Gráfico de datas](/exemplos/6.png)

---

## 🔄 Como usar localmente

### Pré-requisitos

- Conversa exportada de um WhatsApp Android (No canto superior direito da conversa, acesse os três pontos, entre em "mais" e exporte a conversa sem mídias)
- Python
- Bibliotecas do requirements.txt

### Executando
Ao executar o programa, um endereço local será exibido no terminal. Acesse esse endereço pelo navegador para utilizar a aplicação.
