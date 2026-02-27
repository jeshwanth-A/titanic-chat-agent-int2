import pandas as pd
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor
from backend.config import GROQ_API_KEY, GROQ_MODEL
from backend.prompts import SYSTEM_PROMPT
from backend.tools import query_data, create_chart
from backend.data_loader import get_dataset_summary


def create_agent(df: pd.DataFrame) -> AgentExecutor:
    llm = ChatGroq(
        api_key=GROQ_API_KEY,
        model=GROQ_MODEL,
        temperature=0,
        max_tokens=4096,
    )

    tools = [query_data, create_chart]

    dataset_summary = get_dataset_summary(df)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                SYSTEM_PROMPT.format(dataset_summary=dataset_summary),
            ),
            MessagesPlaceholder("chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder("agent_scratchpad"),
        ]
    )

    agent = create_tool_calling_agent(llm, tools, prompt)

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=15,
        return_intermediate_steps=True,
    )

    return agent_executor
