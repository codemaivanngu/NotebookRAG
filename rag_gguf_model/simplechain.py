# from langchain.chains import CTransformers
from langchain_community.llms import CTransformers
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

#Cấu hình
model_file = r"C:\Users\Tung\Downloads\models\models\vinallama-7b-chat_q5_0.gguf"
#load llm
def load_llm(model_file):
    # return ctransformers.load(model_file)
    llm = CTransformers(
        model = model_file,
        model_type='llama',
        max_new_tokens= 1024,
        temperature=0.01,
    )
    return llm

#tạo prompt template
def create_prompt(template):
    prompt = PromptTemplate(
        template=template,
        input_variables=['question']
    )
    return prompt
#tạo simple chain
def create_simple_chain(prompt, llm):
    chain = LLMChain(
        prompt=prompt,
        llm=llm,
        # output_key='answer'
    )
    return chain

template = """
<|im_start|>system
Bạn là một trợ lí AI hữu ích. Hãy trả lời người dùng một cách ngắn gọn chính xác.
<|im_end|>
<|im_start|>user
{question}<|im_end|>
<|im_start|>assistant
"""

prompt = create_prompt(template)
print(prompt)
llm = load_llm(model_file)
llm_chain = create_simple_chain(prompt, llm)
question ="1 + 1 bằng mấy?"
response = llm_chain.invoke({'question': question})
print(response)