import PyPDF2
from io import BytesIO

def extract_text_from_pdf(pdf_file):
    """
    从PDF文件中提取文本内容
    :param pdf_file: PDF文件对象或文件路径
    :return: 提取的文本内容
    """
    try:
        # 始终使用文件路径的方式
        text = ""
        with open(pdf_file, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)

            # 获取总页数
            num_pages = len(pdf_reader.pages)
            print(f"PDF文件共有 {num_pages} 页")

            # 逐页提取文本
            for i, page in enumerate(pdf_reader.pages):
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
                    print(f"第 {i+1} 页提取了 {len(page_text)} 个字符")

        result = text.strip()
        print(f"总共提取了 {len(result)} 个字符")
        return result
    except Exception as e:
        raise Exception(f"PDF解析失败: {str(e)}")

def clean_text(text):
    """
    清洗文本，去除冗余字符和格式
    :param text: 原始文本
    :return: 清洗后的文本
    """
    # 去除多余空格和换行符
    cleaned_text = ' '.join(text.split())
    # 去除特殊字符
    cleaned_text = ''.join(c for c in cleaned_text if c.isprintable())
    return cleaned_text