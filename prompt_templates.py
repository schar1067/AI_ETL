

template_system = """You are an assistant that only speaks in Markdown. Do not write text \
    that isn't formatted as markdown. Example formatting: Testing No-Code Workflow \
    --Summary-- This audio recording documents a test of a no-code workflow \
    using Google Drive and a single code step to reduce calls and improve \
    efficiency. --Additional Info-- ## Main Points - point 1 \
    - point 2 ## Action Items - point 1 - point 2 \
    ## Follow Up Questions - point 1 - point 2 ## \
    Potential Arguments Against - point 1 - point 2
    """

template_user = """Write a Title for the transcript that is under 15 words. \
       Then write: "--Summary--" Write "Summary" as a Heading 1. \
        Write a summary of the provided transcript. Then write: \
        "--Additional Info--". Then return a list of the main points \
        in the provided transcript. Then return a list of action items. \
        Then return a list of follow up questions. Then return a list of \
        potential arguments against the transcript. For each list, \
          return a Heading 2 before writing the list items. Limit each \
          list item to 100 words, and return no more than 5 points per \
          list. Transcript: ```{transcript}```
          """
