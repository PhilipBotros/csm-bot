import re

from langchain import ConversationChain
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferWindowMemory
import openai

from context import context_manager


class BaseChat:
    def __init__(self, system_message, k):
        self.system_message = system_message
        self.top_k = k

    @staticmethod
    def get_context(question, top_k, return_score=False):
        context = context_manager.langchain_chroma.similarity_search_with_score(question, k=top_k)
        if return_score:
            context_str = [f"{el[0].page_content}. Similarity score: {el[1]}" for el in context]
        else:
            context_str = [f"{el[0].page_content}" for el in context]
        return context_str

    @staticmethod
    def run_llm(messages):
        llm_output = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages)
        return llm_output['choices'][0]['message']['content']

    @staticmethod
    def format_current_query(question, context):
        message = f"""Question: {question}"
        This is context you can use to answer the question:" 
        {context}"""
        return message

    def generate_messages(self, question, history, context):
        role_to_openai = {"server": "assistant", "client": "user"}
        messages = [{"role": "system", "content": self.system_message}]
        # Append history (last message in history is current one so we skip it)
        for message in history[:-1]:
            messages.append({"role": role_to_openai[message["author"]], "content": message["text"]})
        # Add current query
        messages.append({"role": "user", "content": self.format_current_query(question, context)})
        return messages


class ChatWithContext(BaseChat):
    def __init__(self, k=1):
        system_message = "The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context or history. If the AI does not know the answer to a question, it truthfully says it does not know."
        super().__init__(system_message, k)

    def talk(self, question, history):
        context = self.get_context(question, top_k=self.top_k)
        messages = self.generate_messages(question, history, context)
        return self.run_llm(messages)


class ChatWithContextTree(BaseChat):
    def __init__(self, k=1):
        system_message = """The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context or history. If the AI does not know the answer to a question, it truthfully says it does not know.
        If there are multiple answers, please answer using list items like:
        1.answer 
        2.answer
        3.answer
        """
        super().__init__(system_message, k)

    def talk(self, question, history):
        context = self.get_context(question, top_k=self.top_k)
        messages = self.generate_messages(question, history, context)
        return self.format_answer(self.run_llm(messages))

    @staticmethod
    def format_answer(answer):
        # Splitting using regex
        answers = re.split(r'\d+\.', answer)  # We start from index 1 to skip the empty string before the first "1."

        # Stripping leading and trailing whitespaces
        answers = [answer.strip() for answer in answers]
        answers = [answer for answer in answers if answer]
        return answers


class ChatWithoutContext:
    def __init__(self, k=10):
        self.memory = ConversationBufferWindowMemory(return_messages=True, k=k)
        self.chain = ConversationChain(llm=OpenAI(temperature=0), memory=self.memory)

    def talk(self, question, history):
        return self.chain.run(question)

    def get_context(self, question, top_k, return_score=False):
        return None
