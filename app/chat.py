
def start():
    import os
    import pandas as pd
    import numpy as np
    import sys

    df = pd.read_csv(os.path.join(sys.path[0], 'embeddings.csv'), index_col=0)
    print("start apply")
    df['embeddings'] = df['embeddings'].apply(eval).apply(np.array)
    print("end apply")
    return df


def create_context(

        question, df, max_len=1800, size="ada"
):
    import openai
    from openai.embeddings_utils import distances_from_embeddings, cosine_similarity
    """
    Create a context for a question by finding the most similar context from the dataframe
    """

    # Get the embeddings for the question
    # print("Start embeddings")
    q_embeddings = openai.Embedding.create(input=question, engine='text-embedding-ada-002')['data'][0]['embedding']
    # print("End embeddings")
    # Get the distances from the embeddings
    # print("Start calculating cosine similarity")
    df['distances'] = distances_from_embeddings(q_embeddings, df['embeddings'].values, distance_metric='cosine')
    # print("End calculating cosine similarity")
    returns = []
    cur_len = 0

    # Sort by distance and add the text to the context until the context is too long
    # print("start sort by distance")
    for i, row in df.sort_values('distances', ascending=True).iterrows():

        # Add the length of the text to the current length
        cur_len += row['n_tokens'] + 4

        # If the context is too long, break
        if cur_len > max_len:
            break

        # Else add it to the text that is being returned
        returns.append(row["text"])

    # Return the context
    return "\n\n###\n\n".join(returns)


def answer_question(
        df,
        model="text-davinci-003",
        question="What classes do I need to take to graduate?",
        max_len=1800,
        size="ada",
        debug=False,
        max_tokens=150,
        stop_sequence=None
):
    import openai
    """
    Answer a question based on the most similar context from the dataframe texts
    """
    context = create_context(
        question,
        df,
        max_len=max_len,
        size=size,
    )
    # print("end sort by distance")
    # If debug, print the raw model response
    if debug:
        print("Context:\n" + context)
        print("\n\n")

    try:
        # Create a completions using the questin and context
        response = openai.Completion.create(
            prompt=f"Answer the question based on the context below, and if the question can't be answered based on the context, say \"Unfortunately, I have not been trained to answer that question yet (If you would like to help finacially support the text embedding process, please contact the creators after this presentation)\"\n\nContext: {context}\n\n---\n\nQuestion: {question}\nAnswer:",
            temperature=0,
            max_tokens=max_tokens,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=stop_sequence,
            model=model,
        )
        return response["choices"][0]["text"].strip()
    except Exception as e:
        print(e)
        return ""


################################################################################
### Step 13
################################################################################

def askGPT(question, messages, df):
    import openai
    openai.api_key = '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'
    textcompletions = answer_question(df, question=question, debug=False)
    messages.append({"role": "user", "content": f"{question} ### text embeddings: {textcompletions}"})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    messages.append(
        {"role": response['choices'][0]['message']['role'],"content": response['choices'][0]['message']['content']}
    )
    return {response['choices'][0]['message']['content']}