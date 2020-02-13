# Intention detection with Rasa

We do not use the full capacities of rasa but [only the NLU part](https://rasa.com/docs/rasa/nlu/using-nlu-only/)

#### Quick setup:
> Those commands need to be run in the plant_intent_recognizer/ directory
- Train with:  
 `rasa train nlu`
- Start the server with:  
  `rasa run -m models --enable-api --cors “*” --debug`
- Interact with the server with an HTTP POST request like:  
  `curl localhost:5005/model/parse -d '{"text":"hello"}'`
