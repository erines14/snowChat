import re
import warnings
import sys
sys.path.append('/Users/Erin.Escobar/AppData/Local/miniconda3/envs/test_snowchat/utils')

import html
import re

import streamlit as st
from langchain.callbacks.base import BaseCallbackHandler


image_url = f"{st.secrets['SUPABASE_STORAGE_URL']}/storage/v1/object/public/snowchat/"
gemini_url = image_url + "google-gemini-icon.png?t=2024-05-07T21%3A17%3A52.235Z"
mistral_url = (
    image_url
    + "mistral-ai-icon-logo-B3319DCA6B-seeklogo.com.png?t=2024-05-07T21%3A18%3A22.737Z"
)
openai_url = (
    image_url
    + "png-transparent-openai-chatgpt-logo-thumbnail.png?t=2024-05-07T21%3A18%3A44.079Z"
)
user_url = image_url + "cat-with-sunglasses.png?t=2024-05-07T21%3A17%3A21.951Z"
claude_url = image_url + "Claude.png?t=2024-05-07T21%3A16%3A17.252Z"
meta_url = image_url + "meta-logo.webp?t=2024-05-07T21%3A18%3A12.286Z"
snow_url = image_url + "Snowflake_idCkdSg0B6_6.png?t=2024-05-07T21%3A24%3A02.597Z"
qwen_url = image_url + "qwen.png?t=2024-06-07T08%3A51%3A36.363Z"


def get_model_url(model_name):
    if "qwen" in model_name.lower():
        return qwen_url
    elif "claude" in model_name.lower():
        return claude_url
    elif "llama" in model_name.lower():
        return meta_url
    elif "gemini" in model_name.lower():
        return gemini_url
    elif "arctic" in model_name.lower():
        return snow_url
    return mistral_url


def format_message(text):
    """
    This function is used to format the messages in the chatbot UI.

    Parameters:
    text (str): The text to be formatted.
    """
    text_blocks = re.split(r"```[\s\S]*?```", text)
    code_blocks = re.findall(r"```([\s\S]*?)```", text)

    text_blocks = [html.escape(block) for block in text_blocks]

    formatted_text = ""
    for i in range(len(text_blocks)):
        formatted_text += text_blocks[i].replace("\n", "<br>")
        if i < len(code_blocks):
            formatted_text += f'<pre style="white-space: pre-wrap; word-wrap: break-word;"><code>{html.escape(code_blocks[i])}</code></pre>'

    return formatted_text


def message_func(text, is_user=False, is_df=False, model="gpt"):
    """
    This function is used to display the messages in the chatbot UI.

    Parameters:
    text (str): The text to be displayed.
    is_user (bool): Whether the message is from the user or not.
    is_df (bool): Whether the message is a dataframe or not.
    """
    model_url = get_model_url(model)

    avatar_url = model_url
    if is_user:
        avatar_url = user_url
        message_alignment = "flex-end"
        message_bg_color = "linear-gradient(135deg, #00B2FF 0%, #006AFF 100%)"
        avatar_class = "user-avatar"
        st.write(
            f"""
                <div style="display: flex; align-items: center; margin-bottom: 10px; justify-content: {message_alignment};">
                    <div style="background: {message_bg_color}; color: white; border-radius: 20px; padding: 10px; margin-right: 5px; max-width: 75%; font-size: 14px;">
                        {text} \n </div>
                    <img src="{avatar_url}" class="{avatar_class}" alt="avatar" style="width: 40px; height: 40px;" />
                </div>
                """,
            unsafe_allow_html=True,
        )
    else:
        message_alignment = "flex-start"
        message_bg_color = "#71797E"
        avatar_class = "bot-avatar"

        if is_df:
            st.write(
                f"""
                    <div style="display: flex; align-items: center; margin-bottom: 10px; justify-content: {message_alignment};">
                        <img src="{model_url}" class="{avatar_class}" alt="avatar" style="width: 50px; height: 50px;" />
                    </div>
                    """,
                unsafe_allow_html=True,
            )
            st.write(text)
            return
        else:
            text = format_message(text)

        st.write(
            f"""
                <div style="display: flex; align-items: center; margin-bottom: 10px; justify-content: {message_alignment};">
                    <img src="{avatar_url}" class="{avatar_class}" alt="avatar" style="width: 30px; height: 30px;" />
                    <div style="background: {message_bg_color}; color: white; border-radius: 20px; padding: 10px; margin-right: 5px; margin-left: 5px; max-width: 75%; font-size: 14px;">
                        {text} \n </div>
                </div>
                """,
            unsafe_allow_html=True,
        )


class StreamlitUICallbackHandler(BaseCallbackHandler):
    def __init__(self, model):
        self.token_buffer = []
        self.placeholder = st.empty()
        self.has_streaming_ended = False
        self.has_streaming_started = False
        self.model = model
        self.avatar_url = get_model_url(model)

    def start_loading_message(self):
        loading_message_content = self._get_bot_message_container("Thinking...")
        self.placeholder.markdown(loading_message_content, unsafe_allow_html=True)

    def on_llm_new_token(self, token, run_id, parent_run_id=None, **kwargs):
        if not self.has_streaming_started:
            self.has_streaming_started = True

        self.token_buffer.append(token)
        complete_message = "".join(self.token_buffer)
        container_content = self._get_bot_message_container(complete_message)
        self.placeholder.markdown(container_content, unsafe_allow_html=True)

    def on_llm_end(self, response, run_id, parent_run_id=None, **kwargs):
        self.token_buffer = []
        self.has_streaming_ended = True
        self.has_streaming_started = False

    def _get_bot_message_container(self, text):
        """Generate the bot's message container style for the given text."""
        formatted_text = format_message(text)
        container_content = f"""
            <div style="display: flex; align-items: center; margin-bottom: 10px; justify-content: flex-start;">
                <img src="{self.avatar_url}" class="bot-avatar" alt="avatar" style="width: 30px; height: 30px;" />
                <div style="background: #71797E; color: white; border-radius: 20px; padding: 10px; margin-right: 5px; margin-left: 5px; max-width: 75%; font-size: 14px;">
                    {formatted_text} \n </div>
            </div>
        """
        return container_content

    def display_dataframe(self, df):
        """
        Display the dataframe in Streamlit UI within the chat container.
        """
        message_alignment = "flex-start"
        avatar_class = "bot-avatar"

        st.write(
            f"""
            <div style="display: flex; align-items: center; margin-bottom: 10px; justify-content: {message_alignment};">
                <img src="{self.avatar_url}" class="{avatar_class}" alt="avatar" style="width: 30px; height: 30px;" />
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.write(df)

    def __call__(self, *args, **kwargs):
        pass

import streamlit as st
from snowflake.snowpark.exceptions import SnowparkSQLException

from chain import load_chain

# from utils.snow_connect import SnowflakeConnection
from snowchat_ui import StreamlitUICallbackHandler, message_func
from snowddl import Snowddl

warnings.filterwarnings("ignore")
chat_history = []
snow_ddl = Snowddl()

gradient_text_html = """
<style>
.gradient-text {
    font-weight: bold;
    background: -webkit-linear-gradient(left, red, orange);
    background: linear-gradient(to right, red, orange);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    display: inline;
    font-size: 3em;
}
</style>
<div class="gradient-text">snowChat</div>
"""

st.markdown(gradient_text_html, unsafe_allow_html=True)

st.caption("Talk your way through data")
model = st.radio(
    "",
    options=[
        "Claude-3 Haiku",
        "Llama 3-70B",
        "Qwen 2-72B",
        "Snowflake Arctic",
    ],
    index=0,
    horizontal=True,
)
st.session_state["model"] = model

if "toast_shown" not in st.session_state:
    st.session_state["toast_shown"] = False

if "rate-limit" not in st.session_state:
    st.session_state["rate-limit"] = False

# Show the toast only if it hasn't been shown before
if not st.session_state["toast_shown"]:
    st.toast("The snowflake data retrieval is disabled for now.", icon="👋")
    st.session_state["toast_shown"] = True

# Show a warning if the model is rate-limited
if st.session_state["rate-limit"]:
    st.toast("Probably rate limited.. Go easy folks", icon="⚠️")
    st.session_state["rate-limit"] = False

if st.session_state["model"] == "Mixtral 8x7B":
    st.warning("This is highly rate-limited. Please use it sparingly", icon="⚠️")

INITIAL_MESSAGE = [
    {"role": "user", "content": "Hi!"},
    {
        "role": "assistant",
        "content": "Hey there, I'm Chatty McQueryFace, your SQL-speaking sidekick, ready to chat up Snowflake and fetch answers faster than a snowball fight in summer! ❄️🔍",
    },
]

with open("ui/sidebar.md", "r") as sidebar_file:
    sidebar_content = sidebar_file.read()

with open("ui/styles.md", "r") as styles_file:
    styles_content = styles_file.read()

st.sidebar.markdown(sidebar_content)

selected_table = st.sidebar.selectbox(
    "Select a table:", options=list(snow_ddl.ddl_dict.keys())
)
st.sidebar.markdown(f"### DDL for {selected_table} table")
st.sidebar.code(snow_ddl.ddl_dict[selected_table], language="sql")

# Add a reset button
if st.sidebar.button("Reset Chat"):
    for key in st.session_state.keys():
        del st.session_state[key]
    st.session_state["messages"] = INITIAL_MESSAGE
    st.session_state["history"] = []




st.write(styles_content, unsafe_allow_html=True)

# Initialize the chat messages history
if "messages" not in st.session_state.keys():
    st.session_state["messages"] = INITIAL_MESSAGE

if "history" not in st.session_state:
    st.session_state["history"] = []

if "model" not in st.session_state:
    st.session_state["model"] = model

# Prompt for user input and save
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages:
    message_func(
        message["content"],
        True if message["role"] == "user" else False,
        True if message["role"] == "data" else False,
        model,
    )

callback_handler = StreamlitUICallbackHandler(model)

chain = load_chain(st.session_state["model"], callback_handler)


def append_chat_history(question, answer):
    st.session_state["history"].append((question, answer))


def get_sql(text):
    sql_match = re.search(r"```sql\n(.*)\n```", text, re.DOTALL)
    return sql_match.group(1) if sql_match else None


def append_message(content, role="assistant"):
    """Appends a message to the session state messages."""
    if content.strip():
        st.session_state.messages.append({"role": role, "content": content})


def handle_sql_exception(query, conn, e, retries=2):
    append_message("Uh oh, I made an error, let me try to fix it..")
    error_message = (
        "You gave me a wrong SQL. FIX The SQL query by searching the schema definition:  \n```sql\n"
        + query
        + "\n```\n Error message: \n "
        + str(e)
    )
    new_query = chain({"question": error_message, "chat_history": ""})["answer"]
    append_message(new_query)
    if get_sql(new_query) and retries > 0:
        return execute_sql(get_sql(new_query), conn, retries - 1)
    else:
        append_message("I'm sorry, I couldn't fix the error. Please try again.")
        return None


def execute_sql(query, conn, retries=2):
    if re.match(r"^\s*(drop|alter|truncate|delete|insert|update)\s", query, re.I):
        append_message("Sorry, I can't execute queries that can modify the database.")
        return None
    try:
        return conn.sql(query).collect()
    except SnowparkSQLException as e:
        return handle_sql_exception(query, conn, e, retries)


if (
    "messages" in st.session_state
    and st.session_state["messages"][-1]["role"] != "assistant"
):
    user_input_content = st.session_state["messages"][-1]["content"]

    if isinstance(user_input_content, str):
        callback_handler.start_loading_message()

        result = chain.invoke(
            {
                "question": user_input_content,
                "chat_history": [h for h in st.session_state["history"]],
            }
        )
        append_message(result.content)

if (
    st.session_state["model"] == "Mixtral 8x7B"
    and st.session_state["messages"][-1]["content"] == ""
):
    st.session_state["rate-limit"] = True

    # if get_sql(result):
    #     conn = SnowflakeConnection().get_session()
    #     df = execute_sql(get_sql(result), conn)
    #     if df is not None:
    #         callback_handler.display_dataframe(df)
    #         append_message(df, "data", True)
