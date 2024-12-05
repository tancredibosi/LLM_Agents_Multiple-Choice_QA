# LLM_Agents_Multiple-Choice_QA
**TASK**: Multiple-Choice Question Answering <br>
**METRIC**: Accuracy <br>
**BENCHMARK**: Synthetic legal dataset on the italian "Codice Penale":
 * 71 istances
 * 3 options per question
 * considered only "question", "answer_1", "answer_2", "answer_3" and "correct_answer"

## Objectives
Develop a multi-agent system based on open-source LLM for the classification of the correct answer through Web searches. <br>
The aim of the project is to improve the performances of the LLM without training/fine-tuning.

## Project Structure
**Agent library**: langroid <br>
**Open-source provider**: Ollama
**LLM**: Phi-3.5


Metodo:
Utilizzo di OpenAI Swarm [GitHub,Esempio Financial Analysis]
Sostituire l'utilizzo di modelli closed richiedenti OpenAI API Key con modelli open-source ad accesso gratuito [Esempio Ollama]; si consiglia l'uso di Phi-3-Mini.
4 agenti previsti
Ricerca Riferimenti: agente preposto all'individuazione di riferimenti normativi rilevanti per la classificazione della risposta; laddove menzionati direttamente nella domanda, estrarli (es. tool regex), in caso contrario, formulare una query su Google per la ricerca di riferimenti normativi utili.
Nota: tutte le istanze del benchmark fornito riportano il riferimento normativo in chiaro nella domanda; tuttavia, si richiede comunque l'implementazione della ricerca sul Web al fine di fronteggiare scenari applicativi reali e benchmark alternativi.
Esperto Normattiva: agente preposto al recupero di un testo normativo partendo dal suo riferimento (es. numero, anno).
Utilizzo di Normattiva come banca dati completa e autorevole.
Si allega [script] per l'implementazione del tool riferimento→testo mediante scraping.
Ricerca Risposta: agente finalizzato a riformulare la domanda in una query Google per l'individuazione della risposta corretta.
Formulazione Risposta: utilizzo di testi recuperati da Normattiva [Esperto Normattiva] e Google [Ricerca Risposta] per generazione dell'output.
Valutazione dell'Accuracy sul benchmark fornito.
