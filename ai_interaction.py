from openai import OpenAI
from os import environ
import time


PROMPT_PUBMED = """
    You are given a list of JSON objects containing PUBMED article references in which a given Gene is mentioned.
    
    You must read the text field of the dictionary objects (modelling references) and extract a short, meaningful conclusion about the gene's importance and behavioural influences.
    To do this, select 10 most relevant articles, print their names and use them as reference for your conclusion.
    
    You can format the response as a bullet list of short conclusions, redacted in a helpful, accessible tone.
    """

GENE_INFO_DESC_PROMPT = """
    You are given a set of data including information about protein activity levels across different age groups.
    
    You must create a description of the provided gene's behaviour given its parameter values.
    
    The values are extracted from a volcano plot illustrating the significance of the protein activity, 
    in which the x-axis represents log2(fold_change), and the y-axis, an adjusted p-value of -log10(p-value).
    This means you need to compute the actual p-value yourself, and refer to it as such. Do not mention this process.
    
    The said description must be concise, accurate and tackle the meaning of each data sample. This includes the significance of the gene changes.
    Your tone should fit helpful environment (the content is addressed to a large audience) as it will be used in a web-service for observing gene activity.
    
    Follow this format:
    
    <<Name>> <<purpose and importance>>.
    
    The gene's **activity level** appears to be <<**upregulated/downregulated/normal**>> - <<Short description of its effect>>.

    <<Short description of the **significance level**>>.
    """

DONOR_ANALYSIS_PROMPT = """
    You are given a JSON object containing information about a gene's concentration in different donor samples.
    
    The object contains the gene's name, the significance level of the observations made (given by an adjusted p-value equal to -log10 of the actual p-value),
    and two lists of concentration values for young and elderly donors respectively.
    
    You must create a description of the provided gene's behaviour given its parameter values. It should be concise and accurate, written in a helpful tone.
    Do not use more than 1 short conclusion-phrases for each section. Each phrase should contain enough information to have its own line.
    
    You will take into consideration the distribution of the sample values (are they normally distributed? max one phrase) and the range difference between them, as well as the
    gene's general importance and purpose relative to its mean concentration level.
    
    Follow this format:
    
    <<Given the **significance level** of the previous observations, talk about the sample details and what can be understood from them.>> (this introductory section should be very short)
    
    <<Talk about what the range of values could mean for each age group. One phrase max. Relate the meaning to the role of the gene in organisms.>> (format keywords by placing them between sets of ** and use new lines for each section)
    
    Are there any outliers - and are they relevant?
    """

USER_REQUEST_CONTENT = """
                Gene: Growth/differentiation factor 15
                logFC: 0.8737907642484315
                adjPVal: 7.184809761833215
                """

def callOpenAI(dev_prompt, user_request):
    """ Returns streaming generator for Open AI interrogation.

    :param dev_prompt: Prompt to instruct AI on the desired response format.
    :param user_request: Request to fetch data for.
    :return: Open AI streaming generator
    """
    client = OpenAI(api_key=environ['OPENAI_API_KEY'])

    response = client.chat.completions.create(
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
        ],
        stream=True
    )

    for chunk in response:
        if chunk.choices[0].delta.content:
            yield (chunk.choices[0].delta.content
                   .replace("\n", " \n"))
            time.sleep(0.1)