from openai import OpenAI
from os import environ
from gene_requests import get_pubmed_references

PROMPT1 = """
        You are given different datasets including information about protein activity levels across different age groups.
        You must create a description of the provided gene's behaviour given its parameter values.
        The said description must be concise, accurate and tackle the meaning of each data sample. This includes abnormal values
        and what they might indicate, as well as normal behavioural clues.
        """
PROMPT2 = """
        You are given a set of data including information about protein activity levels across different age groups.
        
        You must create a description of the provided gene's behaviour given its parameter values.
        
        The values are extracted from a volcano plot illustrating the significance of the protein activity, 
        in which the x-axis represents log2(fold_change), and the y-axis, -log10(p-value).
        
        The said description must be concise, accurate and tackle the meaning of each data sample. This includes the significance of the gene changes.
        Your tone should fit helpful environment (the content is addressed to a large audience) as it will be used in a web-service for observing gene activity.
        
        Follow this format:
        Regulation level: <<upregulated/downregulated/normal>> - <<Short description of its effect>>
        Significance level: <<value>> - <<meaning>>
        """
PROMPT_PUBMED = """
            You are given a list of JSON objects containing PUBMED article references in which a given Gene is mentioned.
            
            You must read the text field of the dictionary objects (modelling references) and extract a short, meaningful conclusion about the gene's importance and behavioural influences.
            To do this, select 10 most relevant articles, print their names and use them as reference for your conclusion.
            
            You can format the response as a bullet list of short conclusions, redacted in a helpful, accessible tone.
            """


USER_REQUEST_CONTENT = """
                Gene: Growth/differentiation factor 15
                logFC: 0.8737907642484315
                adjPVal: 7.184809761833215
                """

def callOpenAI(dev_prompt, user_request):
    """

    :param dev_prompt: Prompt to instruct AI on the desired response format.
    :param user_request: Request to fetch data for.
    :return: Open AI generated response
    """
    client = OpenAI(api_key=environ['OPENAI_API_KEY'])

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "developer",
                "content": dev_prompt
            },
            {
                "role": "user",
                "content": user_request
            }
        ]
    )

    response = completion.choices[0].message.content

    print(response)

    return response