# MoneyWise
# 💰 MoneyWise

MoneyWise é uma aplicação web voltada para o controle financeiro pessoal. O sistema permite que o usuário gerencie suas finanças, visualize estatísticas, acompanhe dados da bolsa de valores em tempo real e mantenha o controle de seus gastos e perfil de forma intuitiva.

## 🔧 Tecnologias Utilizadas

- **Frontend:** HTML5, CSS3, JavaScript
- **Backend:** Python + Flask
- **Banco de Dados:** SQLite
- **APIs:** Alpha Vantage / BRAPI (para dados da bolsa)

## 🔐 Funcionalidades

- Cadastro e login de usuários com autenticação via JWT
- Armazenamento seguro de senhas criptografadas
- Tela de dashboard com:
  - Dados em tempo real da bolsa de valores
  - Notícias do mercado (em desenvolvimento)
  - Porcentagem de economia mensal (em desenvolvimento)
- Tela de perfil do usuário
- Responsividade para desktop

## 📁 Estrutura de Pastas

backend/ → código backend (routes, models, auth) 
static/ → imagens, css e JS 
templates/ → páginas HTML renderizadas pelo Flask 
.gitignore → arquivos ignorados pelo Git 
app.py → inicializador da aplicação 
README.md → este arquivo


## 🚀 Como executar o projeto localmente

```bash
git clone https://github.com/seuusuario/moneywise.git
cd moneywise
python -m venv venv
source venv/bin/activate (ou venv\\Scripts\\activate no Windows)
pip install -r requirements.txt
python app.py
