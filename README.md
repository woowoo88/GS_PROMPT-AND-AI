# Mission Control AI

**Integrantes**

Angela Takezawa, RM: 570797
Rodrigo Zambelle, RM: 570425
Rodrigo Fidelis Zarzar Santana, RM: 572454

## Sobre o projeto

Sistema inteligente de monitoramento de uma missão espacial experimental. A
aplicação gera ou recebe telemetria de temperatura, energia, comunicação,
oxigênio e estado do módulo, aplica regras automáticas de segurança e usa o
modelo Llama 3.2 1B via Ollama para analisar riscos e recomendar ações.

O projeto combina duas camadas:

* **Regras determinísticas:** alertas e respostas de emergência continuam
  funcionando mesmo sem conexão com o modelo.
* **IA generativa:** um **system prompt** especializado orienta o Llama a validar os
  alertas e priorizar até três ações para a equipe de controle.

## Funcionalidades

* Geração de dados simulados e três cenários reproduzíveis.
* Monitoramento de cinco parâmetros operacionais.
* Classificação em `NORMAL`, `ATENÇÃO` ou `CRÍTICO`.
* Ativação automática de economia de energia, resfriamento, antena redundante e
  reserva de oxigênio.
* Análise contextual com Llama via API local do Ollama.
* Contingência local identificada claramente quando a IA estiver indisponível.
* Testes automatizados da lógica e da exibição da resposta da IA.

## Demonstracao

### Operacao normal

![Cenario normal](assets/01_cenario_normal.png)

### Parametros em atencao

![Cenario de atencao](assets/02_cenario_atencao.png)

### Situacao critica e respostas automaticas

![Cenario critico](assets/03_cenario_critico.png)

### Analise apresentada pela IA

![Analise da IA](assets/04_analise_ia.png)

## Como executar no Google Colab

Abra o notebook:
[Mission_Control_AI.ipynb](Mission_Control_AI.ipynb)

No GitHub, clique em **Open in Colab** ou acesse:

https://colab.research.google.com/github/woowoo88/GS_PROMPT-AND-AI/blob/main/Mission_Control_AI.ipynb

Execute as celulas em ordem. O notebook instala o Ollama, inicia o servidor,
baixa o modelo `llama3.2:1b` e demonstra cenarios normal e critico.

Ao final da instalacao deve aparecer `TESTE DIRETO DO LLAMA`. As demonstracoes
do Colab usam modo estrito e exibem `ANALISE (LLAMA VIA OLLAMA)`. Se o modelo
nao estiver funcionando, a celula para com erro em vez de apresentar uma
resposta local como se fosse IA.

Se uma execucao anterior falhou durante a instalacao, use
**Ambiente de execucao > Reiniciar sessao** e execute todas as celulas novamente.
O notebook instala o pacote `zstd`, exigido pelas versoes atuais do Ollama.

## Como executar localmente

Requer Python 3.10 ou superior e
[Ollama](https://ollama.com/download).

```bash
ollama serve
ollama pull llama3.2:1b
python mission_control.py --scenario critical
```

Para demonstrar apenas as regras locais, sem iniciar o modelo:

```bash
python mission_control.py --scenario normal --no-ai
python mission_control.py --scenario attention --no-ai
python mission_control.py --scenario critical --no-ai
```

Os cenarios disponiveis sao `normal`, `attention`, `critical` e `random`.

## Testes

```bash
python -m unittest discover -s tests -v
```

## Tecnologias

- Python 3
- Llama 3.2 1B
- Ollama
- Google Colab
- API HTTP local do Ollama
- Pillow para gerar as evidencias visuais

## Decisoes automaticas

| Condicao | Nivel | Resposta |
|---|---|---|
| Temperatura >= 45 C | Critico | Ativar resfriamento de emergencia |
| Energia < 20% | Critico | Economia e desligamento de cargas |
| Sinal < 25% | Critico | Alternar para antena redundante |
| Oxigenio < 90% | Critico | Isolar modulo e ativar reserva |
| Desvio moderado | Atencao | Correcao preventiva correspondente |
