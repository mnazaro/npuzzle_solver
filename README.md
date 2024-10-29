# 8 Puzzle Game

Este é um jogo de quebra-cabeça 8-puzzle implementado em Python. O jogo permite que o usuário mova as peças manualmente e também pode resolver o quebra-cabeça automaticamente usando o algoritmo A*.

## Estrutura do Projeto

- `main.py`: Ponto de entrada do programa.
- `puzzle/`: Contém os módulos principais do jogo.
  - `board.py`: Lógica do tabuleiro.
  - `solver.py`: Algoritmo de resolução automática.
  - `utils.py`: Funções auxiliares.
- `tests/`: Contém os testes unitários.
- `README.md`: Documentação do projeto.
- `requirements.txt`: Dependências do projeto.

## Como Executar

1. Clone o repositório.
2. Instale as dependências:
   ```sh
   pip install -r requirements.txt
   ````
3. Execute o jogo:
   ```sh
   python main.py
   ```
### Testes
Para executar os testes, use o comando:
```bash
python -m unittest discover tests
```


### requirements.txt

```txt
# Adicione aqui as dependências do projeto, se houver
```
Essa estrutura modular facilita a manutenção e a expansão do projeto, permitindo adicionar novas funcionalidades e testes de forma organizada.
