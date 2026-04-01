def get_context(vectorstore, query="Generate DDR report"):
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    docs = retriever.invoke(query)

    return "\n\n".join([doc.page_content for doc in docs])