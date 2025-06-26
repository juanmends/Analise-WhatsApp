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
- ✅ Detecção de autores, palavras, emojis e mídias ocultas
- ✅ Geração de gráficos interativos:
  - **📊 Emojis mais usados**
  - **📅 Dias da semana mais ativos**
  - **📈 Frequência ao longo do tempo**
- ✅ Estatísticas individuais por participante
- ✅ Interface web amigável e fácil de usar

---

## 📷 Demonstrações

> Substitua os caminhos abaixo pelos screenshots reais após executar seu projeto.

### 🔻 Página de upload
![Página de upload](/static/img/upload.png)

### 🔻 Emojis mais usados
![Gráfico de emojis](/static/img/emojis.png)

### 🔻 Atividade por dia da semana
![Gráfico dias da semana](/static/img/dias.png)

### 🔻 Evolução temporal das mensagens
![Gráfico de datas](/static/img/datas.png)

---

## 🔄 Como usar localmente

### Pré-requisitos

- Python 3.8+
- Git instalado

### Instalação

```bash
# Clone o repositório
git clone https://github.com/juanmends/Analise-WhatsApp.git
cd Analise-WhatsApp

# Instale as dependências
pip install -r requirements.txt
