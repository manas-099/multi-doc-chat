import os
import sys
import json
from dotenv import load_dotenv
from MultiDocChat.utils.config_loader import load_config
from MultiDocChat.logger import GLOBAL_LOGGER as log

from MultiDocChat.exceptions.custom_exception import DocumentPortalException
from langchain_google_genai import  ChatGoogleGenerativeAI


class ApiKeysManager:
        REQUIRED_KEYS=['GOOGLE_API_KEY']

        def __init__(self):
                self.api_keys={}
                raw=os.getenv("apikeyliveclass")
                if raw:
                    try:
                        parsed=json.loads(raw)
                        if not isinstance(parsed,dict):
                              raise ValueError("api keys is not a valid json object")
                        self.api_keys=parsed
                    except Exception as e:
                          log.warning("Failed to parse api_keys as json",error=str(e))
        
                for key in self.REQUIRED_KEYS:
                      if not self.api_keys.get(key):
                            env_val=os.getenv(key)
                            if env_val:
                                  self.api_keys[key]=env_val
                                  log.info(f"loaded {key} from individual env var")
                missing=[k for k in self.REQUIRED_KEYS if not self.api_keys.get(k)]
                if missing:
                      log.error("Missing required api keys ",missing_keys=missing)
                      raise DocumentPortalException("missing api keys",sys)
                log.info("API keys loaded", keys={k: v[:6] + "..." for k, v in self.api_keys.items()})
        def get(self, key: str) -> str:
            val = self.api_keys.get(key)
            if not val:
                raise KeyError(f"API key for {key} is missing")
            return val


class ModelLoader:
      def __init__(self):
            if os.getenv("ENV","local").lower() != "production":
                  load_dotenv()
                  log.info("running in local mode:.env loaded")
            else:
                  log.info("running in production mode")
            self.api_key_manager=ApiKeysManager()
            self.config=load_config()
            log.info("YAML CONFIG LOADED")
      def load_embedding_model(self):
            try:
                  model_name=self.config['embedding_model']['model_name']
                  log.info("Loading embedding model",model=model_name)
            except Exception as e:
                  log.error("Error loading embedding model",error=str(e))
                  raise DocumentPortalException("Failed to laod Embeddingmodel",sys)
      def load_llm(self):
            
                    llm_block=self.config['llm']
                    provider_key=os.getenv("LLM_PROVIDER","google")
                    if provider_key not in llm_block:
                            log.error("LLM provider not foumd in config",provider=provider_key)
                            raise ValueError(f"LLM PROVIDER  NOT FOUND in config")
                    llm_config=llm_block[provider_key]
                    provider = llm_config.get("provider")
                
                    model_name = llm_config.get("model_name")
                    temperature = llm_config.get("temperature", 0.2)
                    max_tokens = llm_config.get("max_output_tokens", 2048)

                    log.info("Loading LLM", provider=provider, model=model_name)

                    if provider == "google":
                            return ChatGoogleGenerativeAI(
                                model=model_name,
                                google_api_key=self.api_key_manager.get("GOOGLE_API_KEY"),
                                temperature=temperature,
                                max_output_tokens=max_tokens
                            )
                    else:
                        log.error("Unsupported LLM provider", provider=provider)
                        raise ValueError(f"Unsupported LLM provider: {provider}")
                            
if __name__ == "__main__":
    loader = ModelLoader()

    # Test Embedding
    embeddings = loader.load_embedding_model()
    print(f"Embedding Model Loaded: {embeddings}")


    # Test LLM
    llm = loader.load_llm()
    print(f"LLM Loaded: {llm}")
    result = llm.invoke("Hello, how are you?")
    print(f"LLM Result: {result.content}")