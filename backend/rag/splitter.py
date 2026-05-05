from langchain_text_splitters import RecursiveCharacterTextSplitter

def get_splitter():
    tool = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", "。", " ", ""],
        length_function=len
    )
    return tool
