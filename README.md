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
**Open-source provider**: Ollama <br>
**LLM**: Phi-3.5 <br>

The multi-agent system is composed of 4 agents:
 * **ReferenceFinder**: agent that finds references in the given question, or searchs for them on Google if there are not in the question. <br>Methods:
   * **find_legal_references**: checks for legal references in the input string using regex.
   * **search_web_for_references**: Formulates a Google search query, scrapes titles and descriptions of search results and calls **find_legal_references**
   * **process_question**: agent's policy that calls **find_legal_references** and, if no reference is found, calls **search_web_for_references**. It than outputs the reference found.
 * **NormattivaExpert**: agent responsible to call the NormattivaScraper script to find legal text on https://www.normattiva.it given the input reference. <br>NOTE: NormattivaScraper has been modified to find also the articles of "Codce Penale".
 * **AnswerScraper**: agent that reformulates the input question, performs a Google search, and produces an answer based on them.<br>Methods:
   * **search_google**: performs a Google search given the query and returns the top-5 results
   * **clean_data**: cleans the content of the Google searches given in input and returns a list of dictionaries
   * **find_unique_answer**: gives the question and the data found on Google to the LLM and outputs a unique answer to the question.
   * **get_answer**: policy to perform the whole task using the methods explained before
 * **AnswerCompiler**: agent that takes the input (question, choices, legal text, Google answer) to make it process to an LLM and then extracts the answered choice from the LLM response: 1,2, 3 or 0 (if None is found)

## Requirements
 * python 3.11
 * libraries:
    * langroid
    * ftfy
    * selenium
    * bs4
    * numpy
    * pandas
 * normattiva_scraper.py (file slightly changed) in the same folder of the notebook
 * mcqa_codice_penale.json in the same folder of the notebook
 * "chromedriver" in "/usr/local/bin/" (MAC OS)
