from openai import OpenAI
from os import environ


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
USER_REQUEST_CONTENT = """
                Gene: Growth/differentiation factor 15
                logFC: 0.8737907642484315
                adjPVal: 7.184809761833215
                """

client = OpenAI(api_key=environ['OPENAI_API_KEY'])

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "developer",
            "content": PROMPT2
        },
        {
            "role": "user",
            "content": USER_REQUEST_CONTENT
        }
    ]
)

print(completion.choices[0].message.content)