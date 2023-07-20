import wikipedia
import re
from datetime import date


# CONSTANTS
CONTEXT_CHAR_LIMIT = 4000
CONTEXT_HALF_SIZE = 300
EXCERPT_HALF_SIZE = 200

CONTEXT_DIVIDER = " [...] "
BOLD_SEQUENCE_START = "\033[1m"
BOLD_SEQUENCE_END = "\033[0m"

INTRO_MESSAGE = "\nWelcome to Wikipedia GPT-3 Bot. Ask any question.\n"
REPL_PROMPT = "(wikibot) "


class Wiki_QA:
    def __init__(self, llm) -> None:
        self.llm = llm

    def question_to_page_search_query(self, question):
        prompt = f"""
    Which Wikipedia page would you search for to answer the following question: "{question}"

    Page name:"""

        return self.llm(prompt=prompt)

    def page_search_query_to_page(self, page_search_query):
        search_results = wikipedia.search(page_search_query)

        if len(search_results) == 0:
            return "No Wikipedia pages found to answer the question"

        try:
            return wikipedia.page(search_results[0], auto_suggest=False)
        except wikipedia.DisambiguationError as e:
            return wikipedia.page(e.options[0], auto_suggest=False)

    def gen_completion(self, prompt):
        return self.sanitize_response(self.llm(prompt=prompt))

    def sanitize_response(self, response):
        return response.strip().replace("\n", "").replace('"', "")

    def generate_ctrlf_term(self, page, question):
        prompt = f"""
    Given the Wikipedia page for "{page.title}", what word would you search for on the page to answer the question "{question}" # type: ignore

    Search term:"""

        return self.gen_completion(prompt)

    def generate_context(self, page, ctrlf_term):
        matches = [
            match.start()
            for match in re.finditer(ctrlf_term, page.content, re.IGNORECASE)
        ]

        top_three_contexts = []
        for match in matches:
            if len(top_three_contexts) == 3:
                break

            excerpt = (
                page.content[match - CONTEXT_HALF_SIZE : match + CONTEXT_HALF_SIZE]
                if match > CONTEXT_HALF_SIZE
                else page.content[0 : match + match]
            )

            if excerpt in page.summary:
                continue

            top_three_contexts.append(excerpt.strip())

        return (CONTEXT_DIVIDER.join([page.summary.strip()] + top_three_contexts))[
            :CONTEXT_CHAR_LIMIT
        ]

    def generate_excerpt(self, context, question):
        prompt = f"""
    Background text: 

    "{context}"

    Given the background text above, which substring would you highlight to answer the question "{question}"

    Excerpt:"""

        excerpt = self.gen_completion(prompt)

        if excerpt in context:
            return excerpt
        else:
            return None

    def generate_answer(self, context, question):
        DATE_TODAY = date.today().strftime("%B %d, %Y")

        prompt = f"""
    Background text: 

    "{context}"

    Answer the following question using only the background text above. Today's date is {DATE_TODAY}.

    Question: "{question}"
    Answer:"""

        return self.gen_completion(prompt)

    def answer_question(self, question):
        page_search_query = self.question_to_page_search_query(question)

        page = self.page_search_query_to_page(page_search_query)
        print(f"Pulling up page: {page.title}")

        ctrlf_term = self.generate_ctrlf_term(page, question)

        context = self.generate_context(page, ctrlf_term)

        answer, excerpt = (
            self.generate_answer(context, question),
            self.generate_excerpt(context, question),
        )

        return answer
