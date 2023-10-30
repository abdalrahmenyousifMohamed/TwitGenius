import os
import gradio as gr
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
os.environ["OPENAI_API_KEY"] = "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"
class Chat:
    """A chatbot interface that interacts with LangChain and Gradio UI."""

    def __init__(self):
        self.system_template = ""
        self.llm = None        

    def generate_response(self, openai_api_key,human_message):
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.llm = ChatOpenAI(temperature=0.5, openai_api_key=OPENAI_API_KEY, model_name='gpt-3.5-turbo')
        if self.llm is None:
            raise ValueError("LangChain model is not initialized. Provide an OpenAI API key.")
        
        system_template = """
        You are an AI content strategist with an in-depth understanding of Twitter's ever-evolving landscape.
Your mission is to provide users with content topics that not only align with their preferences but also leverage current events and trending subjects.

% RESPONSE TONE:

- Your responses should exude expertise and foresight.
- Engage users with insightful, thought-provoking, and relevant content suggestions.
- Maintain a friendly and conversational tone throughout.

% RESPONSE FORMAT:

- Offer a range of content topic suggestions that cater to diverse interests.
- If a user shows interest in a specific topic, craft a tweet or a thread that delves deep into that subject.
- Provide clear and concise insights within the character limit.

% RESPONSE CONTENT:

- Analyze the user's tweet for cues about their interests and concerns.
- Stay updated with trending Twitter topics, current events, and conversations.
- Suggest content topics that bridge the user's existing interests with real-time discussions.
- Draft compelling tweets or threads that encourage user engagement and conversation.

Example:

If the user's tweet_text mentions "space exploration," you can respond with:

" Space exploration is an endlessly fascinating topic! Let's discuss the latest discoveries on Mars, the potential for future moon missions, and the role of private companies in the space race. I'll craft a tweet that sparks curiosity and invites others to join the cosmic conversation. Ready for takeoff?"

Remember to stay ahead of the curve and offer content suggestions that keep users engaged and informed in the dynamic world of Twitter.
        """
        
        system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
        human_template = "{text}"
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
        
        final_prompt = chat_prompt.format_prompt(text=human_message).to_messages()
        response = self.llm(final_prompt).content
        print(response)
        response_list = [[response]]

        return response_list

chatbot = Chat()

with gr.Blocks() as demo:
    gr.HTML(
        """<div style="text-align: center; max-width: 700px; margin: 0 auto;">
        <div
        style="
            display: inline-flex;
            align-items: center;
            gap: 0.8rem;
            font-size: 1.75rem;
        "
        >
        <h1 style="font-weight: 900; margin-bottom: 7px; margin-top: 5px;">
            TwitGenius
        </h1>
        </div>
        <p style="margin-bottom: 10px; font-size: 94%">
        Track
        </p>
    </div>"""
    )
    with gr.Row():
        question = gr.Textbox(
            label="Type in your questions about wandb here and press Enter!",
            placeholder="Generate Content ",
        )
        openai_api_key = gr.Textbox(
            type="password",
            label="Enter your OpenAI API key here",
        )
    state = gr.State()
    chatbot_instance = gr.Chatbot()
    question.submit(
        chatbot.generate_response,
        [question, state],
        [chatbot_instance, state],
    )

if __name__ == "__main__":
    demo.queue().launch(
        share=False, server_name="0.0.0.0", server_port=2222, show_error=True
    )
