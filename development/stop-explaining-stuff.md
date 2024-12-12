---
title: "Just Code, No Explanations"
---

## Notes

 My experience using LLMs for code generation has been that they all seem to depart from the assumption that in addition to code snippets, the user is looking for an educational experience in which the LLM both provides code, ie acting as a tutor-by-demonstration.

 Presently, I prefer to segregate these experiences. Sometimes I'm looking for the LLM to simply generate a quick bash script to do something and in other instances. I'd like the LLM to actually explain things about coding to me. But personally I rarely want or desire these two things at the same time

 The strategic idea for this particular system prompt is to specify that the LLM, in addition to providing full code snippets, also should not provide any explanations before or after the actual code generation. By specifying this, not only can you prevent this from happening, you can also preserve as many tokens as possible for the actual code generation part of the output. If you are using natural language prompting to ask LLMs to generate complete Python programs, for example, the continuous output length can frequently pose a challenge to these code generation projects.

 The final instruction in the system prompt is to ask the LLM to not litter their code with lots and lots of comments. The purpose here is again token preservation - to allow as much headroom as possible for actual code generation by wasting as few tokens as possible on explanations that are often not necessary

## System Prompt

Your task is to generate full code programs for the user. You should never provide explanations or anything other than full code programs. You must also never provide code snippets. Even if you are only editing code always include full code. Make sure to never include any comments in the code that you generate