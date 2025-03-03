# Agentic Hairdresser
![architecture](docs/Agentic-workflow-hairdresser.png)
## Overview

Agentic Hairdresser is an AI-powered agentic chatbot that assists customers in booking appointments at a hair salon. The agent interacts dynamically with users to find and confirm available time slots using external tools and APIs.

## Features

* **Conversational Booking:** Guides customers through the appointment scheduling process.

* **AI-Powered:** Uses Anthropic Claude 3.7 Sonnet LLM with instructive prompting to simulate a hairdresser assistant.

* **Google Calendar Integration:** Checks available time slots and creates new bookings upon confirmation.

* **Custom Python Tools:** Fetches business logic data such as hairdresser services and pricing.

* **Speech Support:** Converts speech to text and vice versa for a natural user experience.

## Architecture

* **Speech-to-Text Interface:** Utilizes the SpeechRecognition Python package and a locally deployed OpenAI-Whisper model for audio transcription.

* **LLM Framework:** Built with LangGraph and LangChain, leveraging Claude 3.7 Sonnet for customer interactions.

* **Memory & Checkpoints:** Maintains chat history for a seamless conversation flow.

* **Tool Invocation:**

* Queries Google Calendar API to check and book time slots.

* Calls custom Python functions to retrieve business-related data.

* **Text-to-Speech System:** Uses Eleven Labs models to generate human-like responses.

## How It Works

The agent interacts with the customer via text or speech. It queries Google Calendar for available slots. Upon confirmation, it schedules the appointment.

It can provide additional details on services and pricing. The response is synthesized into speech for voice interactions.

## How to run

To run the agent, ensure you have:

* Python installed

* API keys for Antrophic Claude Sonnet and Eleven Labs

* Required dependencies from requirements.txt

Run the agent with:
`
./run.sh
`
or,
`
python src/app.py
`

## Contact
leonardo.gutierrez@lgsquare.lu