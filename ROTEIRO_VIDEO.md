# Roteiro do video de demonstracao

Duracao recomendada: **2 minutos e 30 segundos**. Limite da atividade:
**3 minutos**.

## 0:00-0:15 - Apresentacao

> Ola, somos [NOMES DOS INTEGRANTES], RMs [NUMEROS]. Este e o Mission Control
> AI, projeto da Global Solution de Prompt and Artificial Intelligence.

Mostre rapidamente os integrantes ou uma tela com nomes e RMs.

## 0:15-0:35 - Objetivo e tecnologias

> O sistema monitora temperatura, energia, comunicacao, oxigenio e status do
> modulo. Regras locais geram alertas e respostas automaticas, enquanto o
> modelo Llama 3.2 1B, executado pelo Ollama, analisa a situacao da missao.

Mostre o README e o notebook aberto no Google Colab.

## 0:35-1:05 - Cenario normal

Execute a celula do cenario normal.

> Neste cenario, todos os parametros estao seguros. O sistema classifica a
> operacao como normal e a IA recomenda manter o monitoramento.

Mostre no output:

- Os cinco parametros monitorados.
- O nivel `NORMAL`.
- A analise identificada como `LLAMA VIA OLLAMA`.

## 1:05-1:55 - Cenario critico

Execute a celula do cenario critico.

> Agora simulamos temperatura elevada, pouca energia, sinal fraco e oxigenio
> abaixo do limite. O sistema identifica nivel critico e responde
> automaticamente.

Mostre com calma:

- Os alertas gerados.
- O modo de economia de energia.
- O resfriamento de emergencia.
- A antena redundante.
- A reserva de oxigenio.
- A resposta do Llama em tempo real.

## 1:55-2:20 - Dados aleatorios e IA

Execute a celula do cenario aleatorio.

> O sistema tambem gera telemetria aleatoria. Cada leitura e avaliada pelas
> regras e enviada para a IA com um prompt especializado em controle de missao.

Mostre que os valores mudaram e que uma nova analise foi produzida.

## 2:20-2:40 - Encerramento

> Assim, o Mission Control AI organiza a telemetria, detecta riscos, toma
> decisoes basicas e usa inteligencia artificial para apoiar a equipe de
> controle. Obrigado.

Finalize mostrando o repositorio no GitHub.

## Antes de gravar

- Preencha nomes e RMs no README e em `entrega.txt`.
- Execute todas as celulas antes para confirmar que o modelo foi baixado.
- Deixe README, notebook e terminal preparados em abas.
- Grave em 720p ou mais, com texto legivel e audio claro.
- Confirme que o video tem menos de 3 minutos.
- Publique o video externamente e adicione somente o link ao README e ao
  `entrega.txt`.
- Nao coloque o arquivo de video dentro do repositorio.
