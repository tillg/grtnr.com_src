## Translation service implementation

We have access to the ChatGPT API and plan to use it for one implementation of the translation service.

### Architecture

The translation service should be completely independent of the rest of the code, and separately testable. It should use ChatGPT with a good prompt that tells it to translate to the other language while maintaining the markdown structure.

The API of the translation service is already defined, the implememntation should provide an implemenation for this API.

### Plan

- Define a detailed architecture in ARCHITECTURE.md
- Select what Python packages could be used to interact with the ChatGPT API. Try to select what is industry standard.
- Build test first. The test process should translate pre-created sample markdowns and let the user read them and review the translations. This can create feedback that could help to improve the prompt.
- Build out the translation service.
- Note: API keys have to be kept as secrets.
