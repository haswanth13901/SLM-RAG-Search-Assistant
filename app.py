import gradio as gr
from search import search_and_ask, doc_and_ask, ask_only
from history import add_to_history, download_txt, download_pdf, clear_history
from docreader import extract_text, MAX_FILE_SIZE_MB

def handle_query(query, uploaded_file, use_search):
    if not query.strip():
        return "Please enter a question."

    if uploaded_file is not None:
        doc_text, error = extract_text(uploaded_file)
        if error:
            return f"⚠️ {error}"
        if doc_text:
            answer, sources, full_response = doc_and_ask(query, doc_text)
        else:
            return "Could not read the file. Please try another document."
    elif use_search:
        answer, sources, full_response = search_and_ask(query)
    else:
        answer, sources, full_response = ask_only(query)

    add_to_history(query, answer, sources)
    return full_response

with gr.Blocks(title="Local Search Bot") as demo:
    gr.Markdown("# Local Search Bot")
    gr.Markdown("A professional AI search assistant powered by phi3:mini + Tavily.")

    with gr.Row():
        with gr.Column(scale=3):
            query_input = gr.Textbox(
                label="Your Question",
                placeholder="Type your question here..."
            )
        with gr.Column(scale=1):
            file_input = gr.File(
                label=f"Upload Document (PDF, TXT, MD) — Max {MAX_FILE_SIZE_MB} MB",
                file_types=[".pdf", ".txt", ".md"]
            )

    use_search = gr.Checkbox(
        label="🌐 Enable Web Search",
        value=True,
        info="ON = searches web via Tavily · OFF = answers from model knowledge only (faster)"
    )

    answer_output = gr.Textbox(label="Answer")
    submit_btn = gr.Button("Submit", variant="primary")
    submit_btn.click(
        fn=handle_query,
        inputs=[query_input, file_input, use_search],
        outputs=answer_output
    )

    gr.Markdown("### Chat History")
    with gr.Row():
        txt_btn = gr.Button("Download as TXT")
        pdf_btn = gr.Button("Download as PDF")
        clear_btn = gr.Button("Clear History", variant="stop")

    txt_file = gr.File(label="TXT Download")
    pdf_file = gr.File(label="PDF Download")
    clear_output = gr.Textbox(label="Status", interactive=False)

    txt_btn.click(fn=download_txt, outputs=txt_file)
    pdf_btn.click(fn=download_pdf, outputs=pdf_file)
    clear_btn.click(fn=clear_history, outputs=clear_output)

demo.launch()