import streamlit as st
import os
from langchain_core.prompts import PromptTemplate

os.environ['GROQ_API_KEY']  # YOUR GROQ API KEY
from langchain_groq import ChatGroq

llm = ChatGroq(
    model = "openai/gpt-oss-120b",
    temperature = 0.7
)

st.title("Restaurant Name Generator")

cuisine = st.sidebar.selectbox("Pick a cuisine type:",
                               ("Italian", "Chinese", "Mexican", "Indian", "French", "Japanese"))

def generate_restaurant_name_and_items(cuisine):
    prompt_template_name = PromptTemplate(
    input_variables = ['cuisine'],
    template = "I want to open a restaurant for {cuisine} food. Suggest a fancy name for the same. Just the name nothing else.")

    name_chain = prompt_template_name | llm

    prompt_template_name = PromptTemplate(
        input_variables = ['restaurant_name'],
        template = "Suggest 10 menu items for {restaurant_name}. Resturn it as a comma seperated value.")

    food_items_chain = prompt_template_name | llm

    restaurant_name = name_chain.invoke(
        {"cuisine": cuisine}
    ).content.strip()

    food_items = food_items_chain.invoke(
        {"restaurant_name": restaurant_name}
    ).content.strip()

    # Convert CSV → list (better for Streamlit)
    food_items_list = [item.strip() for item in food_items.split(",")]

    return restaurant_name, food_items_list


if cuisine:
    restaurant_name, menu_items = generate_restaurant_name_and_items(cuisine)

    st.header(restaurant_name)
    st.subheader("Menu Items")

    for item in menu_items:
        st.write(f"• {item}")