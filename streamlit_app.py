st.title("Health Symptom Checker")
st.info("⚠️ This tool is for educational purposes only. Always consult a doctor for medical advice.")

# Check for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_input = st.chat_input("Describe your symptoms here...")

# Guardrail: Emergency symptoms
serious_keywords = ["chest pain", "trouble breathing", "severe bleeding"]
if user_input and any(k in user_input.lower() for k in serious_keywords):
    st.warning("🚨 These symptoms may be serious. Please seek immediate medical help.")

# Guardrail: Validate input length
elif user_input:
    if len(user_input.strip()) < 10:
        st.warning("Please provide more detailed information about your symptoms.")
    else:
        # Store and display user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Assistant response with safety prompt
        def get_response(prompt):
            system_prompt = (
                "You are a wellness assistant. Offer general lifestyle advice only. "
                "Never diagnose, prescribe, or act as a substitute for a healthcare provider."
            )
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": system_prompt}] +
                         st.session_state.messages +
                         [{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content

        prompt = f"User has these symptoms: {user_input}. Offer general wellness tips only."
        reply = get_response(prompt)
        st.session_state.messages.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.markdown(reply)

